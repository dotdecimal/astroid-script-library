# Copyright (c) 2015 .decimal, Inc. All rights reserved.
# Author:   Andrew Brown

import os.path
import sys
import dicom
sys.path.append("lib")
import thinknode_worker as tn
import dicom_worker as dicom_worker
import rks_worker as rks

iam = tn.authenticate(tn.read_config('thinknode-dec.cfg'))

def run(file_path, iam):

    upload_file_list=[]
    for dirname, dirnames, filenames in os.walk(file_path):
        # print path to all subdirectories first.
        for subdirname in dirnames:
            print(os.path.join(dirname, subdirname))

        # print path to all filenames.
        for filename in filenames:
            if dicom_worker.valid_dicom_filetype(filename) == True:
                upload_file_list.append(os.path.join(dirname, filename))

    # Track what ct sets and structure sets files have been added
    ct_uids = []
    ss_uids = []

    # These lists must be the same size
    meta_data_list = []
    rks_id_list = []

    filtered_upload_file_list = [] # don't include files that are not CT or RTSTRUCT

    # Make the id list and metadatas that will be posted for "pending" patients
    for f in upload_file_list:
        ds = dicom.read_file(f)
        modality = ds.Modality
        # print(ds)
        meta_data = dicom_worker.make_dicom_meta_data(modality, ds.SeriesInstanceUID, ds.PatientID, ds.PatientsName, ds.PatientsSex, ds.PatientsBirthDate)
        # if meta_data not in meta_data_list:
        if modality == 'CT':
            filtered_upload_file_list.append(f)
            if ds.SeriesInstanceUID not in ct_uids:
                print(ds.SeriesInstanceUID)
                rks_id_list.append(ds.SeriesInstanceUID)
                ct_uids.append(ds.SeriesInstanceUID)
                meta_data_list.append(meta_data)
        elif modality == 'RTSTRUCT' and ds.SOPInstanceUID not in ss_uids:
            print(ds.SOPInstanceUID)
            rks_id_list.append(ds.SOPInstanceUID)
            ss_uids.append(ds.SOPInstanceUID)
            meta_data_list.append(meta_data)
            filtered_upload_file_list.append(f)

    # Write "pending" rks entries for patient
    # print(rks_id_list)
    i = 0
    for rks_id in rks_id_list:
        dicom_data = {
            "dicom_obj": tn.none,
            "meta_data": meta_data_list[i]
            }
        rks_id = rks.write_rks_entry(iam, "imported_dicom_file", "dicom_data", rks_id, dicom_data, None, 'planning')
        i += 1

    obj_list_id = dicom_worker.make_dicom_object_from_dir(iam, file_path, filtered_upload_file_list)
    print("ID to Save: " + str(obj_list_id))

    ids = dicom_worker.get_dicom_object_ids(iam, obj_list_id)
    # print(json.dumps(ids))

    for x in ids:
        dicom_worker.calc_dicom_rks_list_item(x, iam)


# Enter list of directories here (each directory will uploaded separately)
dir_list = []

# Kevin's Files
# dir_list.append('C:/Users/kerhart/Desktop/Documents/Astroid/CustomerService/MGH/tps_20170605_164138917/')
# dir_list.append('C:/SvnFolders/SvnSoftware/data/p.d/Proton/Barnes-Jewish File/Phantoms/Brain2/')
# dir_list.append('C:/SvnFolders/SvnSoftware/data/ProKnow/Plan Study 2017/expander/')
# dir_list.append('C:/SvnFolders/SvnSoftware/data/ProKnow/Cranio-Eclipse/')
# dir_list.append('C:/SvnFolders/SvnSoftware/data/ProKnow/Plan Study 2016/Smaller/')
# dir_list.append('C:/SvnFolders/SvnSoftware/data/ProKnow/Plan Study 2017/AAMD/')
# dir_list.append('C:/SvnFolders/SvnSoftware/data/ProKnow/Plan Study 2017/intact_breast/')
# dir_list.append('C:/SvnFolders/SvnSoftware/data/ProKnow/Plan Study 2017/post_mast/')
# dir_list.append('C:/SvnFolders/SvnSoftware/data/Astroid/DICOM/MGH-patients/DCM_testpatientCD/')
# dir_list.append('C:/SvnFolders/SvnSoftware/data/Astroid/DICOM/MGH-patients/DCM_testpatientAP/')
# dir_list.append('C:/SvnFolders/SvnSoftware/data/Astroid/DICOM/MGH-patients/DCM_testpatientGYN/')
# dir_list.append('C:/SvnFolders/SvnSoftware/data/Astroid/DICOM/MGH-patients/CW2/')
# dir_list.append('C:/SvnFolders/SvnSoftware/data/Astroid/DICOM/MGH-patients/DCM_testpatientCW/')
# dir_list.append('S:/CustomerSupport/Employees/Ivan Ramos/KEVIN/')
# dir_list.append('C:/SvnFolders/SvnSoftware/data/ProKnow/TROG-2017/')
# dir_list.append('C:/SvnFolders/SvnSoftware/data/Astroid/DICOM/TG244/DCM_TG244_h&n/')
# dir_list.append('C:/SvnFolders/SvnSoftware/data/ProKnow/Plan Study 2016/Smaller-A/')
# dir_list.append('C:/SvnFolders/SvnSoftware/data/ProKnow/Plan Study 2016/Smaller-B/')
# dir_list.append('C:/SvnFolders/SvnSoftware/data/ProKnow/Plan Study 2016/Original/')
# dir_list.append('C:/SvnFolders/SvnSoftware/data/Astroid/DICOM/UFHO/Prostate/CT-SS/')
# dir_list.append('C:/SvnFolders/SvnSoftware/data/Astroid/DICOM/UFHO/Breast/CT-SS/')
# dir_list.append('C:/SvnFolders/SvnSoftware/data/Astroid/DICOM/UFHO/Brain/CT-SS/')
# dir_list.append('C:/Users/kerhart/Desktop/Documents/Astroid/demo-data/dicom/DCM_testpatientCW/')
# dir_list.append('C:/SvnFolders/SvnSoftware/data/Astroid/DICOM/MGH-patients/DCM_testpatientRP/')
# dir_list.append('C:/SvnFolders/SvnSoftware/data/Astroid/DICOM/MGH-patients/DCM_testpatientSpine/')
# dir_list.append('C:/SvnFolders/SvnSoftware/data/p.d/Electron/Bolus/PhantomAtAllOrientations/FFP/')
# dir_list.append('C:/SvnFolders/SvnSoftware/data/p.d/Electron/Bolus/PhantomAtAllOrientations/HFP/')
# dir_list.append('C:/SvnFolders/SvnSoftware/data/p.d/Electron/Bolus/PhantomAtAllOrientations/FFS/')
# dir_list.append('C:/SvnFolders/SvnSoftware/data/p.d/Electron/Bolus/PhantomAtAllOrientations/HFS/')
# dir_list.append('C:/SvnFolders/SvnSoftware/data/p.d/Electron/Bolus/PhantomAtAllOrientations/HFDL/')
# dir_list.append('C:/SvnFolders/SvnSoftware/data/p.d/Electron/Bolus/PhantomAtAllOrientations/HFDR/')
# Mevion Files
# dir_list.append('C:/Users/kerhart/Desktop/Documents/Astroid/research/Mevion/Cases/Chondrosacorma/')
# dir_list.append('C:/Users/kerhart/Desktop/Documents/Astroid/research/Mevion/Cases/NewChordoma/')
# dir_list.append('C:/Users/kerhart/Desktop/Documents/Astroid/research/Mevion/Cases/Ependynoma_clean/')
# dir_list.append('C:/Users/kerhart/Desktop/Documents/Astroid/research/Mevion/Cases/L_Orbital/')
# dir_list.append('C:/Users/kerhart/Desktop/Documents/Astroid/research/Mevion/Cases/Nasopharynx/')
# dir_list.append('C:/Users/kerhart/Desktop/Documents/Astroid/research/Mevion/Cases/Prostate/')
# dir_list.append('C:/Users/kerhart/Desktop/Documents/Astroid/research/Mevion/Cases/Meningioma_Adjacent_RightOrbit/')
# Georgetown Files
# dir_list.append('C:/Users/kerhart/Desktop/Documents/Astroid/CustomerService/Georgetown/AB001_AB001/')
# dir_list.append('C:/Users/kerhart/Desktop/Documents/Astroid/CustomerService/Georgetown/FH001_FH001/')
# dir_list.append('C:/Users/kerhart/Desktop/Documents/Astroid/CustomerService/Georgetown/HP001_HP001/')
# dir_list.append('C:/Users/kerhart/Desktop/Documents/Astroid/CustomerService/Georgetown/JL001_JL001/')
# dir_list.append('C:/Users/kerhart/Desktop/Documents/Astroid/CustomerService/Georgetown/RM001_RM001/')

## Daniel's Files
# dir_list.append('C:/Users/Dabo/Documentation/Data/ProKnow/Plan Study 2016/Original')
# dir_list.append('C:/Users/Dabo/Documentation/Data/ProKnow/Plan Study 2016/New Patient')
# dir_list.append('C:/Users/Dabo/Documentation/Data/Astroid/DICOM/MGH-patients/DCM_testpatientAnal')
# dir_list.append('C:/Users/Dabo/Documentation/Data/Astroid/DICOM/MGH-patients/DCM_testpatientGYN')
# dir_list.append('C:/Users/Dabo/Documentation/Data/Astroid/DICOM/MGH-patients/DCM_testpatientCW')
# dir_list.append('C:/Users/Dabo/Documentation/Data/Astroid/DICOM/MGH-patients/DCM_testpatientAP')
# dir_list.append('C:/Users/Dabo/Documentation/Data/Astroid/DICOM/MGH-patients/DCM_testpatientRP')
# dir_list.append('C:/Users/Dabo/Documentation/Data/Astroid/DICOM/MGH-patients/DCM_testpatientCD')
# dir_list.append('C:/Users/Dabo/Documentation/Data/p.d/Electron/Bolus/PhantomAtAllOrientations/HFS/')
# dir_list.append('C:/Users/Dabo/Documentation/Data/p.d/Electron/Bolus/PhantomAtAllOrientations/HFP/')
# dir_list.append('C:/Users/Dabo/Documentation/Data/p.d/Electron/Bolus/PhantomAtAllOrientations/FFS/')
# dir_list.append('C:/Users/Dabo/Documentation/Data/p.d/Electron/Bolus/PhantomAtAllOrientations/FFP/')
# dir_list.append('C:/Users/Dabo/Documentation/Data/Proknow/Plan Study 2017/cranio/')
# dir_list.append('C:/Users/Dabo/Documentation/Data/ProKnow/Plan Study 2017/AAMD/')
# dir_list.append('C:/Users/Dabo/Documentation/Data/ProKnow/Plan Study 2017/expander/')
# dir_list.append('C:/Users/Dabo/Documentation/Data/ProKnow/Plan Study 2017/intact_breast/')
# dir_list.append('C:/Users/Dabo/Documentation/Data/ProKnow/Plan Study 2017/post_mast/')
# dir_list.append('C:/Users/Dabo/Documentation/Data/Astroid/DICOM/TG244/DCM_TG244_abdomen')
# dir_list.append('C:/Users/Dabo/Documentation/Data/Astroid/DICOM/TG244/DCM_TG244_anus')
# dir_list.append('C:/Users/Dabo/Documentation/Data/Astroid/DICOM/TG244/DCM_TG244_h&n')
dir_list.append('C:/Users/Dabo/Documentation/Data/Astroid/DICOM/TG244/DCM_TG244_lung')
dir_list.append('C:/Users/Dabo/Documentation/Data/Astroid/DICOM/TG244/DCM_TG244_prostate')


# Upload all patient files in each directory in the list
for d in dir_list:
    run(d, iam)
