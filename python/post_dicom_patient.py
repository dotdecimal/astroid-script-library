# Copyright (c) 2015 .decimal, Inc. All rights reserved.
# Author:   Andrew Brown/Daniel Patenaude
# Date:     09/25/2015
# Desc:     Post folder to thinknode and get back a dicom_patient

import os.path
from lib import thinknode_worker as thinknode
from lib import dicom_worker as dicom
from lib import decimal_logging as dl

# Get IAM ids
iam = thinknode.authenticate(thinknode.read_config('thinknode.cfg'))
 
# Create a study
study_id = dicom.make_rt_study_from_dir(iam, 'E:/dicom/MGH_Phantom_min/')

# Combine uploaded CT image slices into an Image_3d datatype
study_calc = \
  thinknode.function(iam["account_name"], 'dicom', "merge_ct_image_slices",
      [
          thinknode.reference(study_id)
      ])
study_res = thinknode.do_calculation(iam, study_calc, False)
dl.data("Patient rt_tudy ISS ID: ", study_res)