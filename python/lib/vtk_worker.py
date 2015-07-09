# Copyright (c) 2015 .decimal, Inc. All rights reserved.
# Author:   Daniel Patenaude
# Date:     07/08/2015
# Desc:     Worker to perform vtk file writing based on named type

# Write a VTK file for an image3
#   param file_path: file path where VTK can be created
#   param image: triangle_mesh object to get decoded
def write_vtk_image3(file_path, image):

    # Create output stream and open
    stream = open(file_path, 'w')

    # Write header information
    stream.write("# vtk DataFile Version 2.0\n")
    stream.write("CRADLE IMAGE3\n")
    stream.write("ASCII\n")
    stream.write("DATASET RECTILINEAR_GRID\n")

    coords = ["X", "Y", "Z"]

    # Write rectilinear grid coordinates to stream
    stream.write("DIMENSIONS " + str(image['size'][0] + 1) + " " + str(image['size'][1] + 1) + " " + str(image['size'][2] + 1) + "\n")
    for k in range(0,3):
        n = image['size'][k] + 1
        origin = image['origin'][k]
        step = image['axes'][k][k]
        stream.write(coords[k] + "_COORDINATES " + str(n) + " double\n")
        for i in range(0,n):
            stream.write(str(origin + i * step) + " ")
        stream.write("\n")

    # Write cell data to stream
    pixel_count = image['size'][0] * image['size'][1] * image['size'][2]
    stream.write("CELL_DATA " + str(pixel_count) + "\n")
    stream.write("SCALARS pixels double\n")
    stream.write("LOOKUP_TABLE default\n")
    for i in range(0, pixel_count):
        stream.write(str(image['pixels'][i] * image['value_mapping']['slope'] + image['value_mapping']['intercept']) + "\n")

    # Close stream
    stream.close()


# Write a VTK file for an image2
#   param file_path: file path where VTK can be created
#   param image: triangle_mesh object to get decoded
def write_vtk_image2(file_path, image):

    # Create output stream and open
    stream = open(file_path, 'w')

    # Write header information
    stream.write("# vtk DataFile Version 2.0\n")
    stream.write("CRADLE IMAGE3\n")
    stream.write("ASCII\n")
    stream.write("DATASET UNSTRUCTURED_GRID\n")

    # Write vertices to stream
    ni = image['size'][0]
    nj = image['size'][1]
    stream.write("POINTS " + str(ni * nj) + " double\n")
    k = 0
    originX = image['origin'][0]
    originY = image['origin'][1]
    stepX = image['axes'][0][0]
    stepY = image['axes'][1][1]
    for j in range(nj):
        for i in range(ni):
            stream.write(originX + str(double(i) * stepX) + " " + str(originY + double(j) * stepY) + " " + image['pixels'][k] + "\n")
            k += 1

    # Write faces to stream
    face_count = (image['size'][0] - 1) * (image['size'][1] -1)
    stream.write("CELLS " + str(face_count) + " " + str(face_count * 5) + "\n")
    for j in range(nj - 1):
        for i in range(ni - 1):
            stream.write("4 " + str(j * ni + i) + " " + str((j+1) * ni + i) + " " + str((j+1) * ni + i + 1) + " " + str(j * ni + i + 1) + "\n")

    # Write cell types to stream
    stream.write("CELL_TYPES " + face_count + "\n")
    for i in range(face_count):
        stream.write("7\n")

    # Close stream
    stream.close()


# Write a VTK file for a triangle mesh
#   param file_path: file path where VTK can be created
#   param mesh: triangle_mesh object to get decoded
def write_vtk_triangle_mesh(file_path, mesh):

    # Create output stream and open
    stream = open(file_path, 'w')

    # Write header information
    stream.write("# vtk DataFile Version 2.0\n")
    stream.write("CRADLE TRIANGLE MESH\n")
    stream.write("ASCII\n")
    stream.write("DATASET UNSTRUCTURED_GRID\n")

    # Write vertices to stream
    stream.write("POINTS " + str(len(mesh['vertices'])) + " double\n")
    for i in range(len(mesh['vertices'])):
        stream.write(str(mesh['vertices'][i][0]) + " " + str(mesh['vertices'][i][1]) + " " + str(mesh['vertices'][i][2]) + "\n")

    # Write faces to stream
    face_count = int(len(mesh['faces']))
    stream.write("CELLS " + str(face_count) + " " + str(face_count*4) + "\n")
    for i in range(face_count):
        stream.write("3 " + str(mesh['faces'][i][0]) + " " + str(mesh['faces'][i][1]) + " " + str(mesh['faces'][i][2]) + "\n")

    # Write cell types to stream
    stream.write("CELL_TYPES " + str(face_count) + "\n")
    for i in range(face_count):
        stream.write("7\n")

    # Close stream
    stream.close()


# Write a VTK file for a list of coordinates
#   param file_path: file path where VTK can be created
#   param points: list of x, y, z points to get decoded
def write_vtk_vector3d(file_path, points):

    # Create output stream and open
    stream = open(file_path, 'w')

    # Write header information
    stream.write("# vtk DataFile Version 2.0\n")
    stream.write("CRADLE TRIANGLE MESH\n")
    stream.write("ASCII\n")
    stream.write("DATASET UNSTRUCTURED_GRID\n")

    # Write vertices to stream
    stream.write("POINTS " + str(len(points)) + " double\n")
    for i in range(len(points)):
        stream.write(str(points[i][0]) + " " + str(points[i][1]) + " " + str(points[i][2]) + "\n")

    # Write cells to stream
    stream.write("CELLS " + str(len(points)) + " " + str(len(points) * 2) + "\n")
    for i in range(len(points)):
        stream.write("1 " + str(i) + "\n")

    # Write cell types to stream
    stream.write("CELL_TYPES " + str(len(points)) + "\n")
    for i in range(len(points)):
        stream.write("1\n")

    # Close stream
    stream.close()

# Write a VTK file for a polyset
#   param file_path: file path where VTK can be created
#   param poly: polyset object to get decoded
#   param z: double for level in the Z direction of the polygon (optional)
def write_vtk_polyset(file_path, poly, z=0):

    # Create output stream and open
    stream = open(file_path, 'w')

    # Write header information
    stream.write("# vtk DataFile Version 2.0\n")
    stream.write("CRADLE POLYSET\n")
    stream.write("ASCII\n")
    stream.write("DATASET POLYDATA\n")

    # Count the points
    polygon_count = len(poly['polygons'])
    v_count = 0
    for i in range(polygon_count):
        v_count += len(poly['polygons'][i]['vertices'])

    # Write vertices to stream
    stream.write("POINTS " + str(v_count) + " double\n")
    buff = "POLYGONS " + str(polygon_count) + " " + str(v_count + polygon_count) + "\n"
    j = 0
    for i in range(polygon_count):
        vertex_count = len(poly['polygons'][i]['vertices'])
        buff += str(vertex_count)
        for k in range(vertex_count):
            v1 = poly['polygons'][i]['vertices'][k]
            stream.write(v1[0] + " " + v1[1] + " " + str(z) + "\n")
            buff += " " + str(j)
            j += 1
        buff += "\n"

    # Write polygon's indices to stream
    stream.write(buff)

    # Close stream
    stream.close()