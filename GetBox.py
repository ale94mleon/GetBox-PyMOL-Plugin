# -*- coding: utf-8 -*-
from random import randint

from pymol import cmd
from pymol.cgo import *
from pymol.vfont import plain

##############################################################################
# GetBox Plugin.py --  Draws a box surrounding a selection and gets box information
# This script is used to get box information for LeDock, Autodock Vina and AutoDock Vina.
# Copyright (C) 2014 by Mengwu Xiao (Hunan University)
#
# USAGES:  See function GetBoxHelp()
# REFERENCE:  drawBoundingBox.py  written by  Jason Vertrees
# EMAIL: mwxiao AT hnu DOT edu DOT cn
# Changes:
# 2014-07-30 first version was uploaded to BioMS http://bioms.org/forum.php?mod=viewthread&tid=1234
# 2018-02-04 uploaded to GitHub https://github.com/MengwuXiao/GetBox-PyMOL-Plugin
#            fixed some bugs: python 2/3 and PyMOL 1.x are supported;
#            added support to AutoDock;
#            added tutorials in English;
# NOTES:
# This program is free software; you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See
# the GNU General Public License for more details.
##############################################################################


def __init__(self):
    self.menuBar.addcascademenu('Plugin', 'GetBox Plugin', 'GetBox PyMOL Plugin', label='GetBox Plugin')
    self.menuBar.addmenuitem('GetBox Plugin', 'command', 'getbox_help', label='Help', command=lambda s=self: getbox_help())
    self.menuBar.addmenuitem('GetBox Plugin', 'command', 'autobox', label='Autodetect box', command=lambda s=self: autobox())
    self.menuBar.addmenuitem('GetBox Plugin', 'command', 'getbox', label='Get box from selection (sele) ', command=lambda s=self: getbox())
    self.menuBar.addmenuitem('GetBox Plugin', 'command', 'rmhet', label='Remove HETATM ', command=lambda s=self: rmhet())


def getbox_help():
    Usages = '''get latest plugin and tutorials at https://github.com/MengwuXiao/GetBox-PyMOL-Plugin

Usages:
this plugin is a simple tool to get box information for LeDock and Autodock Vina or other molecular docking soft.
Using the following functions to get box is recommended.

* autobox [extending] (NOTES: solvent & some anions will be removed)
    this function autodetects box in chain A with one click of mouse, but sometimes it fails for too many ligands or no ligand
    e.g. autobox

* getbox [selection = (sele), [extending = 5.0]]
    this function creates a box that around the selected objects (residues or ligands or HOH or others).
    Selecting ligands or residues in the active cavity reported in papers is recommended
    e.g. getbox
    e.g. getbox (sele), 6.0

* resibox [Residues String, [extending = 5.0]]
    this function creates a box that arroud the input residues in chain A.
    Selecting residues in the active cavity reported in papers is recommended
    e.g. resibox resi 214+226+245, 8.0
    e.g. resibox resi 234 + resn HEM, 6.0

* showbox [minX, maxX, minY, maxY, minZ, maxZ]
    this function creates a box based on the input axis, used to visualize box or amend box coordinate
    e.g. showbox 2,3,4,5,6,7

 * rmhet
    remove HETATM, remove all HETATM in the screen

Notes:
* If you have any questions or advice, please do not hesitate to contact me (mwxiao AT hnu DOT edu DOT cn), thank you!'''

    print(Usages)


def showaxes(minX, minY, minZ):
    cmd.delete('axes')
    cylinder_width = 0.5
    cylinder_length = 5.0
    obj = [
    CYLINDER, minX, minY, minZ, minX + cylinder_length, minY, minZ, cylinder_width, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0,
    CYLINDER, minX, minY, minZ, minX, minY + cylinder_length, minZ, cylinder_width, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
    CYLINDER, minX, minY, minZ, minX, minY, minZ + cylinder_length, cylinder_width, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0,
    ]
    cyl_text(obj, plain,[minX + cylinder_length, minY, minZ - cylinder_width], 'X', 0.20, axes=[[3, 0, 0], [0, 3, 0], [0, 0, 3]])
    cyl_text(obj, plain,[minX - cylinder_width, minY + cylinder_length, minZ], 'Y', 0.20, axes=[[3, 0, 0], [0, 3, 0], [0, 0, 3]])
    cyl_text(obj, plain,[minX - cylinder_width, minY, minZ + cylinder_length], 'Z', 0.20, axes=[[3, 0, 0], [0, 3, 0], [0, 0, 3]])
    cmd.load_cgo(obj,'axes')


def showbox(minX, maxX, minY, maxY, minZ, maxZ):
    current_view = cmd.get_view()
    cmd.delete('box')
    linewidth = 3.0
    minX = float(minX)
    minY = float(minY)
    minZ = float(minZ)
    maxX = float(maxX)
    maxY = float(maxY)
    maxZ = float(maxZ)
    showaxes(minX, minY, minZ)
    boundingBox = [
        LINEWIDTH, float(linewidth),
        BEGIN, LINES,
        # x lines
        COLOR, 1.0, 0.0, 0.0, 	        # red
        VERTEX, minX, minY, minZ,       # 1
        VERTEX, maxX, minY, minZ,       # 5

        VERTEX, minX, maxY, minZ,       # 3
        VERTEX, maxX, maxY, minZ,       # 7

        VERTEX, minX, maxY, maxZ,       # 4
        VERTEX, maxX, maxY, maxZ,       # 8

        VERTEX, minX, minY, maxZ,       # 2
        VERTEX, maxX, minY, maxZ,       # 6
        # y lines
        COLOR, 0.0, 1.0, 0.0, 	        # green
        VERTEX, minX, minY, minZ,       # 1
        VERTEX, minX, maxY, minZ,       # 3

        VERTEX, maxX, minY, minZ,       # 5
        VERTEX, maxX, maxY, minZ,       # 7

        VERTEX, minX, minY, maxZ,       # 2
        VERTEX, minX, maxY, maxZ,       # 4

        VERTEX, maxX, minY, maxZ,       # 6
        VERTEX, maxX, maxY, maxZ,       # 8
        # z lines
        COLOR, 0.0, 0.0, 1.0,		    # blue
        VERTEX, minX, minY, minZ,       # 1
        VERTEX, minX, minY, maxZ,       # 2

        VERTEX, minX, maxY, minZ,       # 3
        VERTEX, minX, maxY, maxZ,       # 4

        VERTEX, maxX, minY, minZ,       # 5
        VERTEX, maxX, minY, maxZ,       # 6

        VERTEX, maxX, maxY, minZ,       # 7
        VERTEX, maxX, maxY, maxZ,       # 8

        END
        ]
    boxName = "box"
    # while boxName in cmd.get_names():
    #     boxName = "box"
    cmd.load_cgo(boundingBox, boxName)
    # Restore the previous view settings
    cmd.set_view(current_view)
    SizeX = maxX - minX
    SizeY = maxY - minY
    SizeZ = maxZ - minZ
    CenterX = (maxX + minX)/2
    CenterY = (maxY + minY)/2
    CenterZ = (maxZ + minZ)/2
    BoxCode = "BoxCode(" + boxName + ") = showbox %0.1f, %0.1f, %0.1f, %0.1f, %0.1f, %0.1f" % (minX, maxX, minY, maxY, minZ, maxZ)
    # output LeDock input file
    LeDockBox = "*********LeDock Binding Pocket*********\n" + \
        "Binding pocket\n%.1f %.1f\n%.1f %.1f\n%.1f %.1f\n" % (minX, maxX, minY, maxY, minZ, maxZ)
    # output AutoDock Vina input file
    VinaBox = "*********AutoDock Vina Binding Pocket*********\n" + \
        "--center_x %.1f --center_y %.1f --center_z %.1f --size_x %.1f --size_y %.1f --size_z %.1f\n" % (CenterX, CenterY, CenterZ, SizeX, SizeY, SizeZ)
    # output AutoDock box information
    # add this function in 2016-6-25 by mwxiao
    AutoDockBox = "*********AutoDock Grid Option*********\n" + \
        "npts %d %d %d # num. grid points in xyz\n" % (SizeX/0.375, SizeY/0.375, SizeZ/0.375) + \
        "spacing 0.375 # spacing (A)\n" + \
        "gridcenter %.3f %.3f %.3f # xyz-coordinates or auto\n" % (CenterX, CenterY, CenterZ)

    print(VinaBox)
    print(AutoDockBox)
    print(LeDockBox)
    print(BoxCode)
    # cmd.zoom(boxName)
    # cmd.show('surface')
    return boxName


def show_vinabox(center_x, center_y, center_z, size_x, size_y, size_z):

    center_x = float(center_x)
    center_y = float(center_y)
    center_z = float(center_z)
    size_x = float(size_x)
    size_y = float(size_y)
    size_z = float(size_z)

    minX = center_x - size_x / 2
    minY = center_y - size_y / 2
    minZ = center_z - size_z / 2
    maxX = center_x + size_x / 2
    maxY = center_y + size_y / 2
    maxZ = center_z + size_z / 2

    showbox(
        minX=minX,
        maxX=maxX,
        minY=minY,
        maxY=maxY,
        minZ=minZ,
        maxZ=maxZ
    )


def getbox(selection="(sele)", extending=5.0):
    # cmd.hide("spheres")
    # cmd.show("spheres", selection)
    ([minX, minY, minZ], [maxX, maxY, maxZ]) = cmd.get_extent(selection)
    minX = minX - float(extending)
    minY = minY - float(extending)
    minZ = minZ - float(extending)
    maxX = maxX + float(extending)
    maxY = maxY + float(extending)
    maxZ = maxZ + float(extending)
    # cmd.zoom(showbox(minX, maxX, minY, maxY, minZ, maxZ))
    showbox(minX, maxX, minY, maxY, minZ, maxZ)


# remove ions
def removeions():
    cmd.select("Ions", "((resn PO4) | (resn SO4) | (resn ZN) | (resn CA) | (resn MG) | (resn CL)) & hetatm")
    cmd.remove("Ions")
    cmd.delete("Ions")


# autodedect box
def autobox(extending=5.0):
    cmd.remove('solvent')
    removeions()
    cmd.select("ChainAHet", "hetatm & chain A")  # found error in pymol 1.8 change "chain a" to "chain A"
    getbox("ChainAHet", extending)


# remove hetatm
def rmhet(extending=5.0):
    cmd.select("rmhet", "hetatm")
    cmd.remove("rmhet")


# GetBox from cavity residues that reported in papers
def resibox(ResiduesStr="", extending=5.0):
    cmd.select("Residues", ResiduesStr + " &  chain A")
    getbox("Residues", extending)


cmd.extend("getbox", getbox)
cmd.extend("showbox", showbox)
cmd.extend("show_vinabox", show_vinabox)
cmd.extend("autobox", autobox)
cmd.extend("resibox", resibox)
cmd.extend("getbox_help", getbox_help)
cmd.extend("rmhet", rmhet)
