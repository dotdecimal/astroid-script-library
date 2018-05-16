# Copyright (c) 2015 .decimal, LLC. All rights reserved.
# Author:   Andrew Brown/Daniel Patenaude
# Date:     09/25/2015
# Desc:     Post folder to thinknode and get back a dicom_patient


import sys
sys.path.append("lib")
import thinknode_worker as thinknode
import dicom_worker as dicom
import decimal_logging as dl

# Get IAM ids
iam = thinknode.authenticate(thinknode.read_config('thinknode.cfg'))
 
#  Set the location of the DICOM files (CTs and SS)
dir_name = 'C:/Users/kerhart/Desktop/Documents/Astroid/demo-data/dicom/DCM_testpatientCD'

# Create a study
study_id = dicom.make_rt_study_from_dir(iam, dir_name)

# Combine uploaded CT image slices into an Image_3d datatype
study_calc = \
  thinknode.function(iam["account_name"], 'dicom', "merge_ct_image_slices",
      [
          thinknode.reference(study_id)
      ])
study_res = thinknode.do_calculation(iam, study_calc, False)
dl.data("Patient rt_tudy ISS ID: ", study_res) # Make note of this ID to use in other scripts as needed