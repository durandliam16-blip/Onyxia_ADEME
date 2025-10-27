echo 'lancement du télechargement'

curl -L -o mssql-1.24.0.vsix https://github.com/microsoft/vscode-mssql/releases/download/v1.24.0/mssql-1.24.0.vsix 

code-server --install-extension mssql-1.24.0.vsix
