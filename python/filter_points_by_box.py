import json
import sys
sys.path.append("lib")
import thinknode_worker as thinknode
import dosimetry_worker as dosimetry
import rt_types as rt
import decimal_logging as dl

# Get Identify Access Management configuration
iam = thinknode.authenticate(thinknode.read_config('thinknode.cfg'))

box = rt.box_3d()
box.corner = [0., 0., 0.]
box.size = [2., 2., 2.]

points = (
  [1.,1.,1.], #This one will be in the box
  [10.,1.,1.],
  [1.,-10.,1.],
  [1.,1.,10.],
)

# Calculate what's in the box
filter_points_by_box_calc = \
    thinknode.function(iam["account_name"], "dosimetry", "filter_points_by_box",
        [
           thinknode.value(box.expand_data()),
           thinknode.value(points)
        ])
filter_points_by_box_calc_id = thinknode.do_calculation(iam, filter_points_by_box_calc, False)
filter_points_by_box_result = thinknode.get_immutable(iam, "dosimetry", filter_points_by_box_calc_id, False)

print(filter_points_by_box_result)
