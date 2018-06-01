"""D5C4 scoring function

Based on original matlab code from Gustavo A. Stolovitzky and Robert Prill


"""
from dreamtools.core.challenge import Challenge
import pandas as pd
from dreamtools.core.rocs import D3D4ROC
import numpy as np


class D5C4(Challenge, D3D4ROC):
    """A class dedicated to D5C4 challenge

    Thomas Moerman: 
        * added some fixes using the '_ints' function to make it work with Python 3.4+
        * the problem: float values cannot be intepreted as ints for indexing        
    ::

        from dreamtools import D5C4
        s = D5C4()
        filename = s.download_template()
        s.score(filename)

    Data and templates are downloaded from Synapse. You must have a login.

    """
    def __init__(self, verbose=True, download=True, **kargs):
        """.. rubric:: constructor

        """
        super(D5C4, self).__init__('D5C4', verbose, download, **kargs)
        self._init()
        self.sub_challenges = []

    def _init(self):
        # should download files from synapse if required.
        if self._standalone is True:
            return

        # Get goldstandard and unpack zipped files
        self._download_data('D5C4_goldstandard.zip', 'syn4564722')
        self.unzip('D5C4_goldstandard.zip')

        # the probabilities
        self._download_data('D5C4_probabilities.zip', 'syn4564719')
        self.unzip('D5C4_probabilities.zip')

        # the templates
        self._download_data('D5C4_templates.zip', 'syn4564726')
        self.unzip('D5C4_templates.zip')

    def _load_network(self, filename):
        df = pd.read_csv(filename, header=None, sep='[ \t]', engine='python')
        df[0] = df[0].apply(lambda x: x.replace('g','').replace('G',''))
        df[1] = df[1].apply(lambda x: x.replace('g','').replace('G',''))
        df = df.astype(float) # imoprtant for later to check for equality
        return df

    def download_template(self):
        # should return full path to a template file
        filenames = []
        for tag in [1,3,4]:
            filename = "DREAM5_NetworkInference_myteam_Network%s.txt" % tag
            filenames.append(self.get_pathname(filename))
        return filenames

    def download_goldstandard(self):
        # should return full path to a gold standard file
        filenames = []
        for tag in [1,3,4]:
            filename = "DREAM5_NetworkInference_Edges_Network%s.tsv" % tag
            filenames.append(self.get_pathname(filename))
        return filenames
    
    def score(self, filenames):

        assert len(filenames) == 3
        print("The 3 files must be ordered as network 1, 3 and 4")
        res1 = self.score_challengeA(filenames[0], 1)
        res3 = self.score_challengeA(filenames[1], 3)
        res4 = self.score_challengeA(filenames[2], 4)

        aupr = -np.mean(np.log10([res1['p_aupr'], res3['p_aupr'], res4['p_aupr']]))
        auroc = -np.mean(np.log10([res1['p_auroc'], res3['p_auroc'], res4['p_auroc']]))
        print(aupr, auroc, np.mean([aupr, auroc]))

        df = pd.Series()
        df['Overall Score'] = np.mean([aupr, auroc])
        df['AUPR (pvalue)'] = aupr
        df['AUROC pvalue)'] = auroc
        df['Net1 AUPR'] = res1['aupr']
        df['Net3 AUPR'] = res3['aupr']
        df['Net4 AUPR'] = res4['aupr']
        df['Net1 AUROC'] = res1['auroc']
        df['Net3 AUROC'] = res3['auroc']
        df['Net4 AUROC'] = res4['auroc']
        df['Net1 p-aupr'] = res1['p_aupr']
        df['Net3 p-aupr'] = res3['p_aupr']
        df['Net4 p-aupr'] = res4['p_aupr']
        df['Net1 p-auroc'] = res1['p_aupr']
        df['Net3 p-auroc'] = res3['p_aupr']
        df['Net4 p-auroc'] = res4['p_aupr']

        return df

    # copy and paste from D5C3 ' FIXME use classes to factorise code
    def score_challengeA(self, filename, tag):
        """

        :param filename:
        :param tag:
        :return:
        """
        assert tag in [1,3,4]
        tag = str(tag)

        if tag == '1':
            goldfile = self.download_goldstandard()[0]
        elif tag == '3':
            goldfile = self.download_goldstandard()[1]
        elif tag == '4':
            goldfile = self.download_goldstandard()[2]

        # gold standard edges only
        predictionfile = filename

        # precomputed probability densities for various metrics
        pdffile_aupr  = self.get_pathname('Network%s_AUPR.mat' % tag)
        pdffile_auroc = self.get_pathname('Network%s_AUROC.mat'% tag)

        # load probability densities
        pdf_aupr  = self.loadmat(pdffile_aupr)
        pdf_auroc = self.loadmat(pdffile_auroc)

        self.pdf_auroc = self.loadmat(pdffile_auroc)
        self.pdf_aupr = self.loadmat(pdffile_aupr)

        # load gold standard
        self.gold_edges = self._load_network(goldfile)

        # load predictions
        self.prediction = self._load_network(predictionfile)

        # DISCOVERY
        # In principle we could resuse ROCDiscovery class but
        # here the pvaluse were also computed. let us do it here for now

        merged = pd.merge(self.gold_edges, self.prediction, how='inner', on=[0,1])
        self.merged = merged

        TPF = len(merged)
        # unique species should be 1000
        N = len(set(self.gold_edges[0]).union(self.gold_edges[1]))
        # positive
        print('Scanning gold standard')
        # should be 4012, 274380 and 178 on template
        G = self._get_G(self.gold_edges)

        # get back the sparse version for later
        # keep it local to speed up import
        import scipy.sparse
        H = scipy.sparse.csr_matrix(G>0)

        Pos = sum(sum(G > 0))
        Neg = sum(sum(G < 0))
        Ntot = Pos + Neg


        # cleanup the prediction that are in the GS
        self.newpred = self._remove_edges_not_in_gs(self.prediction, G)
        L = len(self.newpred)

        discovery = np.zeros(L)
        X = [tuple(x) for x in _ints(self.newpred[[0,1]].values)-1]
        discovery = [H[x] for x in X]
        TPL = sum(discovery)


        discovery = np.array([int(x) for x in discovery])

        if L < Ntot:
            p = (Pos - TPL) / float(Ntot - L)
        else:
            p = 0

        random_positive_discovery = [p] * (Ntot - L)
        random_negative_discovery = [1-p] * (Ntot - L)

        # append discovery + random using lists
        positive_discovery = np.array(list(discovery) + random_positive_discovery)
        negative_discovery = np.array(list(1-discovery) + random_negative_discovery)

        #  true positives (false positives) at depth k
        TPk = np.cumsum(positive_discovery)
        FPk = np.cumsum(negative_discovery)

        #  metrics
        TPR = TPk / float(Pos)
        FPR = FPk / float(Neg)
        REC = TPR  # same thing
        PREC = TPk / range(1,Ntot+1)

        #  sanity check
        #if ( (P ~= round(TPk(end))) | (N ~= round(FPk(end))) )
        #            disp('ERROR. There is a problem with the completion of the prediction list.')
        #  end

        # finishing touch
        #TPk(end) = round(TPk(end));
        #FPk(end) = round(FPk(end));

        from dreamtools.core.rocs import ROCBase
        roc = ROCBase()
        auroc = roc.compute_auc(roc={'tpr':TPR, 'fpr':FPR})
        aupr = roc.compute_aupr(roc={'precision':PREC, 'recall':REC})

        # normalise by max possible value
        aupr /= (1.-1./Pos)

        p_aupr = self._probability(pdf_aupr['X'][0], pdf_aupr['Y'][0], aupr)
        p_auroc = self._probability(pdf_auroc['X'][0], pdf_auroc['Y'][0], auroc)

        results = {'auroc':auroc, 'aupr':aupr, 'p_auroc':p_auroc, 'p_aupr':p_aupr}
        return results

    def _probability(self, X, Y, x):
        dx = X[1]-X[0]
        return  sum(Y[X >= x])*dx

    def _remove_edges_not_in_gs(self, prediction, G):
        regulators = list(set(prediction[0]))
        targets = list(set(prediction[[0,1]].stack()))

        N, M = G.shape

        # for speeding up, let us get the numpy array values
        data_pred = [tuple(x) for x in _ints(prediction[[0,1]].values)]

        count = 0
        tokeep = []
        for ikeep, row in enumerate(data_pred):
            i, j = row
            if (i <= N) and (j <= M):
                if G[i-1, j-1] != 0:
                    count += 1
                    tokeep.append(ikeep)

        return prediction.copy().ix[tokeep]
    
    def _get_G(self, gold):
        from easydev import Progress
        import scipy.sparse
        regulators = list(set(gold[0]))
        targets = list(set(gold[[0,1]].stack()))

        # [TMO edit]
        N, M = int(gold[0].max()), int(gold[1].max())
        
        ## A will store indices goind from 0 (not 1) to N-1
        # hence the -1 indices when handling A if i,j are the
        # values of the gene
        A = np.zeros((N, M))                
        
        for row in _ints(gold[[0,1]].values):
            i, j = row
            
            # [TMO] edit
            int_i = int(i)
            int_j = int(j)
            
            A[int_i-1, int_j-1] = 1
            
        A_sparse = scipy.sparse.csr_matrix(A)

        #N, M = len(regulators), len(targets)
        G = np.zeros((N, M))

        # pb = Progress(len(regulators), 1)
        for i, x in enumerate(_ints(regulators)):
            for j, y in enumerate(_ints(targets)):
                if A[x-1, y-1] == 1:
                    G[x-1, y-1] = 1
                elif x != y:
                    G[x-1, y-1] = -1
            # pb.animate(i+1)
        return G

def _ints(a):
    return np.asarray(a, dtype=int)