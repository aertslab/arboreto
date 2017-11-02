# Notes

## OOB early stopping heuristic
* http://scikit-learn.org/stable/auto_examples/ensemble/plot_gradient_boosting_oob.html#gradient-boosting-out-of-bag-estimates
* https://gist.github.com/adamwlev/19d2397ff8da1952556cf2417d965f6c
* https://henri.io/posts/using-gradient-boosting-with-early-stopping.html
* paper: _"Early stopping, but when?"_ http://page.mi.fu-berlin.de/prechelt/Biblio/stop_tricks1997.pdf

## IMPORTANT
* add a minimum nr of rounds parameter to the EarlyStopMonitor to prevent premature stopping in case where the loss is negative in the first rounds (cfr. huber loss function).

## Note to self
Ik denk dat ik het laatste irritante probleem in GRNBoost gefixed heb: automatisch bepalen van nr of boosting rounds 
PER REGRESSIE ipv een globale parameter die geschat kan worden maar toch danig wat variatie kan vertonen over de 
regressies heen. De truuk is out-of-bag improvement monitoren, een feature die in scikit-learn gradient boosting zit 
maar niet in xgboost. Tests op de dream data geeft typisch iets minder goed dan net1 (synthetic) en iets beter dan de 
andere (net3 & net4). De 'penalty' is dat je stochastic gradient boosting moet gebruiken (bij elke round een deel van 
de samples aan de kant zetten, pakweg 5% a 10% en die gebruiken als out-of-bag test set voor de heuristic). 
Hoe meer data, hoe minder dit een impact heeft, zegt mijn buikgevoel. Ik zou durven stellen dat we deze boosting method 
als de default kunnen gebruiken, nog eerder dan xgboost. 

## LightGBM
* https://github.com/Microsoft/LightGBM
