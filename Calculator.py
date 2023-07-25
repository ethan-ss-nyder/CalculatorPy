from DisplayFunctions import Display as Disp

Disp.buildGUI()

# Replacement for tkinter's mainloop() function since mainloop() is an absolute thread hogger.
while not(Disp.getExitMainLoop()):
    Disp.window.update_idletasks()
    Disp.window.update()

exit()