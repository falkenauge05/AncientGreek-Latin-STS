#!/bin/bash
# $1: input_file 1 (.vec file)
# $2: input_file 2 (.vec file)
# $3: threshold
# $4: goldstandard file

python bilingual_nearest_neighbor.py --source_embeddings $1 --target_embeddings $2 --output grc-lat.sim --knn 10 -m csls --cslsknn 20
python filter.py --input grc-lat.sim --output grc-lat.sim.pred -m dynamic -th $3
python bucc_f-score.py -p grc-lat.sim.pred -g $4 > grc-lat.sim.pred.res
