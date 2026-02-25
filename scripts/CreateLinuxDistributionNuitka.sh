python -m nuitka \
  --standalone \
  --enable-plugin=pyside6 \
  --linux-icon=RepTate/gui/Images/RepTate_logo_new.png \
  --output-dir=dist \
  --noinclude-qt-translations \
  --include-module=RepTate.gui.Reptate_rc \
  --include-module=RepTate.gui.About_rc \
  --include-module=RepTate.gui.Theory_rc \
  --include-module=RepTate.gui.Tool_rc \
  --include-module=RepTate.gui.MainWindow_rc \
  --include-package=RepTate.tools \
  --include-data-dir=data=data \
  --include-data-dir=RepTate/gui/Images=RepTate/gui/Images \
  --include-data-files=RepTate/tools/*.npy=RepTate/tools/ \
  --include-data-files=RepTate/theories/*.npz=RepTate/theories/ \
  --include-data-files=RepTate/theories/*_linux*.so=RepTate/theories/ \
  --python-flag=-m \
  RepTate
