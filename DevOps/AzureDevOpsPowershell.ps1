
# Script by Mr O - Entellectual Services Limited
# Use this to convert exported JSON files from Microsoft Sentinel

param (
    [Parameter(Mandatory = $false)]$PathToFiles = ('/Users/Desktop/Usecase/sentinel/'),
    [Parameter(Mandatory = $false)]$OutputPath = ('/Users/Desktop/Usecase/converted/')
)


#check to ensure powershell-yaml is installed
if($null -eq (Get-Command ConvertTo-Yaml -errorAction SilentlyContinue)) {
    Write-Error "Module powershell-yaml is missing.  Please install it 'Import-Module powershell-yaml'"
}

if (!(Test-Path -Path ($PathToFiles))) {
    write-host  "Error:  Path to files doesnt exist!" -ForegroundColor Red
}

if (!(Test-Path -Path ($OutputPath))) {
    write-host "Output path doesnt existing, creating..." -ForegroundColor yellow 
    new-item -itemType "directory" -path $OutputPath
}

$files = Get-ChildItem -path $($PathToFiles + "/*") -File -Include *.json
foreach ($file in $files) {
    if (Test-Path $file) {
        $data = Get-Content $file | convertfrom-json -AsHashtable
        foreach ($convertfile in $data.resources) {
            $workspace_item = [ordered]@{}
            $workspace_item['$schema'] = 'https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#'
            $workspace_item['contentVersion'] = '1.0.0.0'
            $workspace_item["parameters"] = @{}
            $workspace_item["parameters"]["workspace"] = @{}
            $workspace_item["parameters"]["workspace"]['type'] = "String"
            $workspace_item["resources"] = @($convertfile)
            if ($workspace_item["resources"][0]["properties"]["query"]) {
                #Clean up the query format
                Write-Verbose "Cleaning up the Query format!"
                $workspace_item["resources"][0]["properties"]["query"] = $workspace_item["resources"][0]["properties"]["query"] -replace "\\n", "`n" -replace '\\"', '"' -replace "`n", "`t`n" -replace "`r", "`t"
            }
            Write-Verbose ('Converting ' + $workspace_item["resources"][0]["properties"]["displayName"]) 

            $displayName = $workspace_item["resources"][0]["properties"]["displayName"] -replace '[\/\s]','_'
            $targetFile  = "$OutputPath$displayName`_ARM.yml"

            $targetDir = Split-Path $targetFile
            if (!(Test-Path $targetDir)) { New-Item -ItemType Directory -Path $targetDir -Force | Out-Null } 

            $workspace_item | ConvertTo-Yaml | Out-File -FilePath $targetFile
            #$workspace_item | ConvertTo-yaml  | Out-File -filepath "$($OutputPath + ($($workspace_item["resources"][0]["properties"]["displayName"]) -replace '[\s]','_'))_ARM.yml"
            $workspace_item = [ordered]@{}
        }
    }
}
