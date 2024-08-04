# Author-Dave2ooo
# Description-Export components with varying parameters as 3mf files.

import adsk.core, adsk.fusion, adsk.cam, traceback, os, sys, math


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
	ui = app.userInterface

        des = adsk.fusion.Design.cast(app.activeProduct)

        # get active design
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)

        # get all components in this design
        allComps = design.allComponents

        # get the script location
        scriptDir = os.path.dirname(os.path.realpath(__file__))

        # create a single exportManager instance
        exportMgr = design.exportManager

        # state the name of the parameter
        paramName1 = "diameter"

        param1 = des.allParameters.itemByName(paramName1)
        if not param1:
            ui.messageBox('The parameter "' + paramName1 + '" must exist.')
            return

        for diameter in range(3, 16):
            param1.value = diameter

			# Update the view and watch the progress
            adsk.doEvents()

            # export the component one by one with a specified format
            for comp in allComps:
				compName = comp.name
                fileName = (scriptDir + "/" + compName + "_par" + str(diameter))

                # export the component with 3mf format
                fileOptions = exportMgr.createC3MFExportOptions(comp)
                fileOptions.meshRefinement = (adsk.fusion.MeshRefinementSettings.MeshRefinementMedium)
                fileOptions.filename = fileName
                exportMgr.execute(fileOptions)

        ui = app.userInterface
        ui.messageBox("Script finished")
    except:
        if ui:
            ui.messageBox("Failed:\n{}".format(traceback.format_exc()))
