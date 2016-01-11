#!/bin/bash

## run as:
## qsub -N assay1 -o $HOME/benchmark -j y submit.sh

CONFIG_PATH=$HOME/Projects/clustercellprofiler1
SOFT_PATH=$HOME/soft/CellProfiler-2.1.1
JOB_PATH=$TMPDIR/$$
OUTPUT_PATH=$HOME/benchmark/$JOB_NAME-$JOB_ID
mkdir -p $OUTPUT_PATH

##$ -o path -j y
##$ -N name
##$ -cwd
##$ -wd working_dir

#$ -pe smp 1
#$ -l membycore=1G
#$ -l runtime=00:25:00
#$ -q debug.q

module load VIGRA/1.10.0-goolf-1.4.10
module load Java/1.7.0_21

source $HOME/soft/cellprofiler_venv/bin/activate
#$ -v LD_LIBRARY_PATH=$EBROOTJAVA/jre/lib/amd64/server:$LD_LIBRARY_PATH

echo
echo 'Peparing job...'
echo
time python $CONFIG_PATH/prepare_job.py $JOB_PATH
echo
echo 'Creating Batch_data.h5...'
echo
time python $SOFT_PATH/CellProfiler.py --do-not-build --do-not-fetch -b -c -r -p $CONFIG_PATH/HeadlessCreateBatch.cppipe -i $JOB_PATH -o $JOB_PATH 
echo
echo 'Running CellProfiler...'
echo
time python $SOFT_PATH/CellProfiler.py --do-not-build --do-not-fetch -b -c -r -p $JOB_PATH/Batch_data.h5 -d $JOB_PATH/CP_DONE 
cd $JOB_PATH
echo
echo 'Cleaning working dorectory...'
echo
rm Batch_data.h5
rm image_sets.csv
rm -rf images
echo
echo 'Creating tar and copying it to home'
echo
tar cvf output.tar *
mv output.tar $OUTPUT_PATH
