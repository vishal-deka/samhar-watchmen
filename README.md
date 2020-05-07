# WatchMen: An anti-crowding system backed by Artificial Intelligence

WatchMen is a system that uses CCTV cameras to detect and report crowding using state of the art crowd counting algorithm proposed in the paper [**From Open Set to Closed Set: Supervised Spatial Divide-and-Conquer for Object Counting**](https://arxiv.org/pdf/2001.01886.pdf).
The code for the above paper has been made available in https://github.com/xhp-hust-2018-2011/S-DCNet and the same is used as a base in this project.
The 'Network' subdirectory contains the implementation of the actual network and has been left untouched.

The working of the system has been described below:

The crowd counting half:
1. Security cameras, or any camera in general will send images in pre-set periodic intervals, say, 5 seconds. The images will be named as cameraID_yyyymmdd-hhmmss (for eg, 12345_20200502-124532). It may do it via http POST requests.
2. The central server receives these images and updates a globa queue where it inserts the names of the images.
3. The crowd counting engine then grabs images in pre-defined batches from this queue and does the required computation.
4. To keep implementation simple, SQLite has been used as the database server. A database containing camera IDs and corresponding location coordinates must be available beforehand. The prediction process will update the timestamp and people count to the database in real time.
5. Alterntively, there is provision in the code to store prediction data in CSV files. The CSV data can then be used for a variety of applications like graphing, setting rules for report, etc.

The reporting half:
1. For the purposes of this hackathon, a simple example has been shown which can be used by authorities to monitor the situation and ensure that social-distancing is being strictly enforced. A browser based GUI has been shown for demonstration purpoes which is still under development. The GUI shall refresh automatically after certain intervals with updated information.
2. Another prominent application is to use other Machine Learning algorithms to make predictions based on the data collected from the WatchMen system.