!ifndef REPTATEVERSION
    !error "REPTATEVERSION must be defined"
!endif
 
!ifndef REPTATEDATE
    !error "REPTATEDATE must be defined"
!endif

!ifndef REPTATEBUILD
    !error "REPTATEBUILD must be defined"
!endif

!include "MUI2.nsh"

!define MUI_ICON "RepTate\icons\Reptate64.ico"
!define MUI_STARTMENUPAGE_DEFAULTFOLDER "RepTate"
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "RepTate\Reptate_license.rtf"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY

;Start Menu Folder Page Configuration
Var StartMenuFolder
!define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKCU" 
!define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\RepTate" 
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"
!insertmacro MUI_PAGE_STARTMENU "RepTate" $StartMenuFolder

!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH
!insertmacro MUI_LANGUAGE "English"

LangString DESC_RepTate ${LANG_ENGLISH} "Install RepTate software"
LangString DESC_FileAssoc ${LANG_ENGLISH} "Associate common RepTate files (*.tts, *.osc, *.shear, etc) with the software"

# Version must be with the format x.x.x.x
!define VERSION "1.0.0.0"
Name "RepTate ${REPTATEVERSION}"
OutFile "RepTateInstaller-${REPTATEVERSION}_${REPTATEDATE}.exe"
InstallDir "$PROGRAMFILES64\RepTate"
InstallDirRegKey HKLM "Software\RepTate" "Install_Dir"
#LicenseData "RepTate\Reptate_license.rtf"
#AddBrandingImage left 100u
VIProductVersion ${VERSION}
VIAddVersionKey "ProductName" "RepTate"
VIAddVersionKey "Comments" "Authors: Jorge Ramirez, Victor Boudara"
VIAddVersionKey "LegalCopyright" "© UPM, ULeeds"
VIAddVersionKey "FileDescription" "Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments"
VIAddVersionKey "FileVersion" ${VERSION}

Section "RepTate ${REPTATEVERSION}" SectionRepTate
	#SetBrandingImage "RepTate\gui\Images\logo_with_uni_logo.png"
	SetOutPath $INSTDIR
	File /r "RepTate\*"
	WriteUninstaller "$INSTDIR\Uninstall RepTate.exe"

	!insertmacro MUI_STARTMENU_WRITE_BEGIN "RepTate"

	;Create shortcuts
	CreateDirectory "$SMPROGRAMS\$StartMenuFolder"
	CreateShortcut "$SMPROGRAMS\$StartMenuFolder\RepTate.lnk" "$INSTDIR\Scripts\RepTate.exe" "" "$INSTDIR\icons\Reptate64.ico"
	CreateShortcut "$SMPROGRAMS\$StartMenuFolder\RepTateCL.lnk" "$INSTDIR\Scripts\RepTateCL.exe" "" "$INSTDIR\icons\Calculator.ico"
	CreateShortcut "$SMPROGRAMS\$StartMenuFolder\MatDB.lnk" "$INSTDIR\Scripts\MatDB.exe" "" "$INSTDIR\icons\DataTable3D.ico"
	CreateShortcut "$SMPROGRAMS\$StartMenuFolder\Uninstall RepTate.lnk" "$INSTDIR\Uninstall RepTate.exe"

	!insertmacro MUI_STARTMENU_WRITE_END
SectionEnd

Section "File Associations" SectionFileAssociations

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

	!insertmacro AssocAddFileExtAndProgId HKCR "$INSTDIR\Scripts\RepTate.exe" ".OSC" "RepTate.OSC" "$INSTDIR\icons\OSC.ico"
	!insertmacro AssocAddFileExtAndProgId HKCR "$INSTDIR\Scripts\RepTate.exe" ".TTS" "RepTate.TTS" "$INSTDIR\icons\LVE.ico"
	!insertmacro AssocAddFileExtAndProgId HKCR "$INSTDIR\Scripts\RepTate.exe" ".SHEAR" "RepTate.SHEAR" "$INSTDIR\icons\NLVE.ico"	
	!insertmacro AssocAddFileExtAndProgId HKCR "$INSTDIR\Scripts\RepTate.exe" ".UEXT" "RepTate.UEXT" "$INSTDIR\icons\NLVE.ico"	
	!insertmacro AssocAddFileExtAndProgId HKCR "$INSTDIR\Scripts\RepTate.exe" ".REAC" "RepTate.REAC" "$INSTDIR\icons\React.ico"	
	!insertmacro AssocAddFileExtAndProgId HKCR "$INSTDIR\Scripts\RepTate.exe" ".GPC" "RepTate.GPC" "$INSTDIR\icons\MWD.ico"	
	!insertmacro AssocAddFileExtAndProgId HKCR "$INSTDIR\Scripts\RepTate.exe" ".GT" "RepTate.GT" "$INSTDIR\icons\Gt.ico"	
	!insertmacro AssocAddFileExtAndProgId HKCR "$INSTDIR\Scripts\RepTate.exe" ".SANS" "RepTate.SANS" "$INSTDIR\icons\SANS.ico"	
	!insertmacro AssocAddFileExtAndProgId HKCR "$INSTDIR\Scripts\RepTate.exe" ".DLS" "RepTate.DLS" "$INSTDIR\icons\Dielectric.ico"	
	!insertmacro AssocAddFileExtAndProgId HKCR "$INSTDIR\Scripts\RepTate.exe" ".CREEP" "RepTate.CREEP" "$INSTDIR\icons\Creep.ico"	
	!insertmacro AssocAddFileExtAndProgId HKCR "$INSTDIR\Scripts\RepTate.exe" ".LAOS" "RepTate.LAOS" "$INSTDIR\icons\LAOS.ico"	
	!insertmacro AssocAddFileExtAndProgId HKCR "$INSTDIR\Scripts\RepTate.exe" ".SHEARXS" "RepTate.SHEARXS" "$INSTDIR\RepTate\gui\Images\Crystal.ico"	

SectionEnd

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
	!insertmacro AssocDeleteFileExtAndProgId HKLM ".LAOS" "RepTate.LAOS"
	!insertmacro AssocDeleteFileExtAndProgId HKLM ".SHEARXS" "RepTate.SHEARXS"

	!insertmacro MUI_STARTMENU_GETFOLDER "RepTate" $StartMenuFolder

	Delete "$SMPROGRAMS\$StartMenuFolder\RepTate.lnk"
	Delete "$SMPROGRAMS\$StartMenuFolder\RepTateCL.lnk"
	Delete "$SMPROGRAMS\$StartMenuFolder\Uninstall RepTate.lnk"
	RMDir "$SMPROGRAMS\$StartMenuFolder"

	DeleteRegKey /ifempty HKCU "Software\RepTate"

	
SectionEnd

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
!insertmacro MUI_DESCRIPTION_TEXT ${SectionRepTate} $(DESC_RepTate)
!insertmacro MUI_DESCRIPTION_TEXT ${SectionFileAssociations} $(DESC_FileAssoc)
!insertmacro MUI_FUNCTION_DESCRIPTION_END
