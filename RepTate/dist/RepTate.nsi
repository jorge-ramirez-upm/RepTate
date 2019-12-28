# Version must be with the format x.x.x.x
!define VERSION "0.9.6.0"
!define DATE "20191111"
Name "RepTate v${VERSION}"
OutFile "RepTate Installer - v${VERSION} ${DATE}.exe"
Icon "RepTate\gui\Images\Reptate64.ico"
InstallDir "$PROGRAMFILES64\RepTate"
InstallDirRegKey HKLM "Software\RepTate" "Install_Dir"
LicenseData "RepTate\Reptate_license.rtf"
#AddBrandingImage left 100u
VIProductVersion ${VERSION}
VIAddVersionKey "ProductName" "RepTate"
VIAddVersionKey "Comments" "Authors: Jorge Ramirez, Victor Boudara"
VIAddVersionKey "LegalCopyright" "© UPM, ULeeds"
VIAddVersionKey "FileDescription" "Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments"
VIAddVersionKey "FileVersion" ${VERSION}

Page license
Page components
Page directory
Page instfiles
UninstPage uninstConfirm
UninstPage instfiles

Section "RepTate v${VERSION}"
	# TEST MessageBox
	#Messagebox MB_OK|MB_ICONINFORMATION \
	#"This is a sample that shows how to use line breaks for larger commands in NSIS scripts"
	#SetBrandingImage "RepTate\gui\Images\logo_with_uni_logo.png"
	SetOutPath $INSTDIR
	File /r "RepTate\*"
	WriteUninstaller "$INSTDIR\Uninstall RepTate.exe"
SectionEnd

Section "Start Menu Shortcuts"

  CreateDirectory "$SMPROGRAMS\RepTate"
  CreateShortcut "$SMPROGRAMS\RepTate\Uninstall.lnk" "$INSTDIR\Uninstall RepTate.exe" "" "$INSTDIR\Uninstall RepTate.exe" 0
  CreateShortcut "$SMPROGRAMS\RepTate\RepTate.lnk" "$INSTDIR\RepTate.exe" "" "$INSTDIR\RepTate.exe" 0
  
SectionEnd


Section "File Associations"

	!macro AssocAddFileExtAndProgId _hkey _exe _dotext _pid _ico
	ReadRegStr $R0 ${_hkey} ${_dotext} ""  ; read current file association
	StrCmp "$R0" "" +3  ; is it empty
	StrCmp "$R0" ${_pid} +2  ; is it our own
		WriteRegStr ${_hkey} ${_dotext} "backup_val" "$R0"  ; backup current value
	WriteRegStr ${_hkey} ${_dotext} "" ${_pid}  ; set our file association
	
	ReadRegStr $R1 ${_hkey} ${_pid} ""
	StrCmp $R1 "" 0 +4
		WriteRegStr ${_hkey} ${_pid} "" ${_pid}
		WriteRegStr ${_hkey} "${_pid}\shell" "" "open"
		WriteRegStr ${_hkey} "${_pid}\DefaultIcon" "" "${_ico}"
	WriteRegStr ${_hkey} "${_pid}\shell\open\command" "" '"${_exe}" "%1"'
	WriteRegStr ${_hkey} "${_pid}\shell\edit" "" "Edit ${_pid}"
	WriteRegStr ${_hkey} "${_pid}\shell\edit\command" "" '"${_exe}" "%1"'
	!macroend

	!insertmacro AssocAddFileExtAndProgId HKCR "$INSTDIR\RepTate.exe" ".OSC" "RepTate.OSC" "$INSTDIR\gui\Images\OSC.ico"
	!insertmacro AssocAddFileExtAndProgId HKCR "$INSTDIR\RepTate.exe" ".TTS" "RepTate.TTS" "$INSTDIR\gui\Images\LVE.ico"
	!insertmacro AssocAddFileExtAndProgId HKCR "$INSTDIR\RepTate.exe" ".SHEAR" "RepTate.SHEAR" "$INSTDIR\gui\Images\NLVE.ico"	
	!insertmacro AssocAddFileExtAndProgId HKCR "$INSTDIR\RepTate.exe" ".UEXT" "RepTate.UEXT" "$INSTDIR\gui\Images\NLVE.ico"	
	!insertmacro AssocAddFileExtAndProgId HKCR "$INSTDIR\RepTate.exe" ".REAC" "RepTate.REAC" "$INSTDIR\gui\Images\React.ico"	
	!insertmacro AssocAddFileExtAndProgId HKCR "$INSTDIR\RepTate.exe" ".GPC" "RepTate.GPC" "$INSTDIR\gui\Images\MWD.ico"	
	!insertmacro AssocAddFileExtAndProgId HKCR "$INSTDIR\RepTate.exe" ".GT" "RepTate.GT" "$INSTDIR\gui\Images\Gt.ico"	
	!insertmacro AssocAddFileExtAndProgId HKCR "$INSTDIR\RepTate.exe" ".SANS" "RepTate.SANS" "$INSTDIR\gui\Images\SANS.ico"	
	!insertmacro AssocAddFileExtAndProgId HKCR "$INSTDIR\RepTate.exe" ".DLS" "RepTate.DLS" "$INSTDIR\gui\Images\Dielectric.ico"	
	!insertmacro AssocAddFileExtAndProgId HKCR "$INSTDIR\RepTate.exe" ".CREEP" "RepTate.CREEP" "$INSTDIR\gui\Images\Creep.ico"	

SectionEnd

UninstallText "This will uninstall example2. Hit next to continue."
UninstallIcon "RepTate\gui\Images\Reptate64.ico"

Section "Uninstall"
	#Delete "$INSTDIR\*"
	RMDir /r "$INSTDIR"
	RMDir /r "$SMPROGRAMS\RepTate"
	
	!macro AssocDeleteFileExtAndProgId _hkey _dotext _pid
	ReadRegStr $R0 ${_hkey} "Software\Classes\${_dotext}" ""
	StrCmp $R0 "${_pid}" 0 +2
		DeleteRegKey ${_hkey} "Software\Classes\${_dotext}"

	DeleteRegKey ${_hkey} "Software\Classes\${_pid}"
	!macroend

	!insertmacro AssocDeleteFileExtAndProgId HKLM ".OSC" "RepTate.OSC"
	!insertmacro AssocDeleteFileExtAndProgId HKLM ".TTS" "RepTate.TTS"
	!insertmacro AssocDeleteFileExtAndProgId HKLM ".SHEAR" "RepTate.SHEAR"
	!insertmacro AssocDeleteFileExtAndProgId HKLM ".REAC" "RepTate.REAC"
	!insertmacro AssocDeleteFileExtAndProgId HKLM ".GPC" "RepTate.GPC"
	!insertmacro AssocDeleteFileExtAndProgId HKLM ".GT" "RepTate.GT"
	!insertmacro AssocDeleteFileExtAndProgId HKLM ".SANS" "RepTate.SANS"
	!insertmacro AssocDeleteFileExtAndProgId HKLM ".DLS" "RepTate.DLS"
	!insertmacro AssocDeleteFileExtAndProgId HKLM ".CREEP" "RepTate.CREEP"
	
SectionEnd


#Function .onInit
#  MessageBox MB_YESNO "This will install RepTate on your Windows PC. Do you wish to continue?" IDYES gogogo
#    Abort
#  gogogo:
#FunctionEnd
