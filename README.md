# cellprofiler-cluster

Notes of CellProfiler running in the cluster

Objective

To run and benchmark CellProfiler 2.1.1 headless in the cluster
Adapt a pipeline created in GUI to create a batch file
Run cellprofiler in the cluster using the batch file as input
Benchmark different ways to process the dataset

Step 1: Creating files and directories specific to the pipeline

Requires original pipeline created with GUI (e.g., ExampleHuman.cppipe)
Requires file list (from GUI: load some images, export image_sets.cvs. It will be used as a template to populate with more files)
The add_modules_pipeline.py python script will replace image import modules by LoadData module. It will also append the CreateBatchFiles modules to the pipeline.

> python add_modules_pipeline.py ExampleHuman.cppipe
> ls
ExampleHuman-LoadDataCreateBatch.cppipe

Step 2: Specific, runs as part of the submit script.

Load required modules, and define paths
The script prepare_job.py creates job folder, copies the the necessary images to a local folder, and creates the image_sets.csv files. The steps related to the images are specific to the pipeline and need to be adjusted accordingly.
Run CellProfiler headless to generate Batch_data.h5. Requires image_sets.cvs

> python CellProfiler.py --do-not-build --do-not-fetch -c -r \
         -p ExampleHuman-LoadDataCreateBatch.cppipe \
         -i job_path -o job_path
> ls
Batch_data.h5

Notes: ExampleHuman-LoadDataCreateBatch.cppipe defines default input and output folders as '.'. When creating Batchdata.h5, it is necessary to use -i and -o arguments, for defining the actual job directories. This values will be set inside Batch_data.h5.

Run CellProfiler headless, input Batch_data.h5

> python CellProfiler.py --do-not-build --do-not-fetch -c -r -p Batch_data.h5
> ls
output files

Installation, configuration, and comments

Currently, CellProfiler is not system-wide-installed. It is a working installation in a personal account.
The installation in the cluster is on progress, it will require some time given the complexity of the dependencies.
Links: http://www.cellprofiler.org/forum/viewtopic.php?f=18&t=3976, Comments on difficult to install ion cluster: http://www.cellprofiler.org/forum/viewtopic.php?f=18&t=3919

CellProfiler Demo

Pipeline: ExampleHuman.cppipe (from CellProfiler tutorials)
Obtain statistics and outline image
Input: Three images per measurement

Output: Cells.csv, Cytoplasm.csv, Image.csv, Nuclei.csv, and outline image
