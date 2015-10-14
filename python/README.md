# Readme
Copyright (c) 2015 .decimal, Inc. All rights reserved.  
Author:   Daniel Patenaude  
Date:     06/09/2015  

## Requirements

Python Verion Required: 

- Python 34

Packages required to run: 

- requests
- colorama
- jsonpickle

```
   python -m pip install requests  
   python -m pip install colorama  
   python -m pip install jsonpickle  
```

## Provided Example File Usages:
1. post_dose_calc_from_dicom.py
    - Posts a dicom patient (from a directory) and calls a sobp dose calculation from the dicom plan
1. post_calc_request_generic.py
	- Posts calculation request based on a prebuilt json request. 
	- The request example provided uses an already existing iss object referenced by ID (iss_files/aperture_creation_params.json).
2. post_calc_request_sobp_dose.py
	- Manually constructs an entire sobp dose calculation request and all required datatypes. No prior postings to ISS is required for this script to run.
	  All data types are constructed inline with the calling calculation request.
3. post_calc_request_sobp_dose_with_shifter.py
	- Manually constructs an entire sobp dose calculation request and all required datatypes and using a constructed degrader. No prior postings to ISS is required for this script to run.
	  All data types are constructed inline with the calling calculation request or posted with running the python script.
4. post_dicom_patient.py
    - Posts a dicom patient (from a directory) to thinknode ISS and returns the rt_study id
5. post_iss_object_generic.py
    - Posts any prebuilt json named_type dosimetry object to thinknode ISS.
	
## Decimal Provided Libraries:
1. decimal_logging.py
	- Prettified log output. Includes optional file logging, timestamps, message coloring (when run through command windows)
2. rt_types.py
	- Reconstruction of rt_types types in python class format. Includes interdependencies between types (e.g. aperture_creation_params.view requires class multiple_source_view)
	- This types match the manifest for the version specified
3. thinknode_worker.py
	- Main worker to perform thinknode IAM, ISS, and calculation requests.
	- Make sure to update thinknode.cfg prior to trying to authenticate with thinknode (see below)
4. dosimetry_worker.py
    - Provides functions to perform basic dosimetry calculation requests to make complex rt_types
5. dicom_worker.py
    - Provides functions to perform basic dicom parsing and translating into defined rt_types
6. vtk_worker.py
    - Provides functions to write common rt_types into .vtk files to be opened in visualizers (e.g. Paraview)
	- Example Usage:
        # Perform calculation (note: make_water_phantom() is a example function provided in the post_calc_request_sobp_dose.py file)
        res = thinknode.do_calculation(iam, make_water_phantom([-100, -100, -100], [200, 200, 200], [2, 2, 2]), True)
        # Cast result to rt_type 
        img3 = rt_types.image_3d()
        img3.from_json(res)
        vtk.write_vtk_image3('testing_image3.vtk', img3.expand_data())
	
## Thinknode.cfg file syntax:
```json
{
    "basic_user": "<Base64 encoded thinknode username:password>",
    "api_url": "https://<thinknode_account>.thinknode.io/api/v1.0",
    "apps":
    {   
        "dosimetry": 
        {    
            "app_version": "1.0.0-beta1",
            "branch_name": "master"
        },
        "dicom":
        {
            "app_version": "",
            "branch_name": "master"       
        },
        "rt_types":
        {
            "app_version": "",
            "branch_name": "master"         
        }
    }, 
    "realm_name": "<thinknode realm>",
    "account_name": "<thinknode account>"
}
```