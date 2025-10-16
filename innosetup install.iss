; ===================================================================
;  Script de Inno Setup para Detector de Objetos con Haar Cascades
;  Utiliza rutas relativas para portabilidad.
; ===================================================================

; --- Definiciones Globales ---
#define MyAppName "DetectorHaar"
#define MyAppVersion "1.0"
#define MyAppPublisher "JOSPROX MX"
#define MyAppURL "https://josprox.com/"
#define MyAppExeName "DetectorHaar.exe"

; --- Rutas Relativas (modifica aquí si cambias tu estructura) ---
#define SourceDir "dist\DetectorHaar"
#define OutputDir "SalidaInstalador"
#define LicenseFile "txt\licencia.txt"
#define InfoFile "txt\información de instalación.txt"
#define IconFile "img\logo.ico"


[Setup]
; --- Identificación y Nombres ---
AppId={{38C58BE0-FC44-4E13-BE89-CF352EF44FF6}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}

; --- Archivos de Información (usando rutas relativas) ---
LicenseFile={#LicenseFile}
InfoBeforeFile={#InfoFile}
SetupIconFile={#IconFile}

; --- Configuración del Instalador ---
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
ChangesAssociations=no
DisableProgramGroupPage=yes
OutputDir={#OutputDir}
OutputBaseFilename=Setup-{#MyAppName}-{#MyAppVersion}
SolidCompression=yes
WizardStyle=modern

; --- Permisos (instalar solo para el usuario actual es más seguro) ---
PrivilegesRequired=lowest


[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"


[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked


[Files]
; --- Copia todos los archivos de la carpeta de distribución a la carpeta de la aplicación ---
; Esta es una forma más robusta y simple de asegurar que todo se incluya.
Source: "{#SourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs


[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon


[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
