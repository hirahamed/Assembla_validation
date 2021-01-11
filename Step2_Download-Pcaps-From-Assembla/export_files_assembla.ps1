##################
## Written by: Kyle Sunderland
##
## Downloads all files from an assembla project
## Need to change repo_name, api_key, and api_secret for the script to work
##################

$repo_name = "Granular_Controls" # Name of the repo

# personal keys found at: https://app.assembla.com/user/edit/manage_clients
$api_key = "20e5bda25a8bb624a4c3" # Assembla api key
$api_secret = "93b3746c6f258b7bb26cc596e7c022b6dda3161a" # Assembla api secret





$array = @(960, 972, 1063, 1078, 1120, 1125, 1126, 1127, 1131, 1133, 1134, 1135, 1136, 1139, 1145, 1149, 1159, 1160, 1181, 1182, 1183, 1186, 1189, 1193, 1204, 1208, 1217, 1221, 1229, 1236, 1250, 1257, 1270, 1279, 1285, 1294, 1068, 1083, 1087, 1088, 1094, 1107, 1119, 1121, 1122, 1123, 1124, 1132, 1151, 1154, 1157, 1166, 1167, 1175, 1177, 1178, 1179, 1195, 1201, 1202, 1206, 1209, 1211, 1218, 1220, 1226, 1253, 1271, 1284, 1291, 1292, 1019, 1089, 1102, 1103, 1105, 1115, 1138, 1142, 1143, 1144, 1150, 1161, 1162, 1187, 1190, 1191, 1192, 1194, 1207, 1242, 1246, 1247, 1251, 1252, 1255, 1263, 1268, 1274, 1275, 1277, 1281, 1286, 1290, 1298, 1299, 1300, 1034, 1049, 1069, 1072, 1085, 1113, 1128, 1129, 1140, 1147, 1156, 1171, 1174, 1180, 1188, 1198, 1200, 1203, 1237, 1240, 1256, 1276, 1280, 1289, 1080, 1082, 1090, 1100, 1110, 1111, 1112, 1118, 1130, 1141, 1148, 1152, 1153, 1155, 1164, 1165, 1168, 1170, 1172, 1199, 1224, 1228, 1230, 1233, 1234, 1238, 1239, 1241, 1243, 1244, 1265, 1269, 1272, 1273, 1287, 1029, 1066, 1074, 1075, 1108, 1109, 1114, 1116, 1117, 1146, 1158, 1163, 1169, 1176, 1185, 1197, 1205, 1210, 1232, 1235, 1248, 1262, 1264, 1267)
foreach ($element in $array) {

    $output_directory = $pwd.Path + "\" + $element + "\"

    If(!(Test-Path $output_directory))
    {
      mkdir $output_directory
    }

    $element
    #$base_uri = "https://api.assembla.com/v1/spaces/Granular-Controls/tickets/$element/attachments.json"
    #$base_uri

    $current_page=1
    $per_page= 1
    $base_uri = "https://api.assembla.com/v1/spaces/Granular-Controls/tickets/$element/attachments.json"
    # $base_uri = "https://api.assembla.com/v1/spaces/" + $repo_name + "/documents.json"
    $base_uri += "?per_page=" + $per_page

    $web_client = New-Object System.Net.WebClient
    $web_client.Headers["X-Api-Key"] = $api_key
    $web_client.Headers["X-Api-Secret"] = $api_secret

    $headers = @{}
    $headers.Add("X-Api-Key", $api_key)
    $headers.Add("X-Api-Secret", $api_secret)

    $number_of_files = 0
    $file_urls = New-Object System.Collections.ArrayList
    $file_names = New-Object System.Collections.ArrayList

    Write-Host "Intezar farmaen"

    # Collect the file names
    Do
    {
      $continue = 1
     

      # Get the current page of files
      $uri = $base_uri + "&page=" + $current_page
      $response = Invoke-WebRequest $uri -Headers $headers -UseBasicParsing

      #Success
      If($response.StatusCode -eq 200)
      {
        # Write-Host "Intezar farmaen aur"
        $document_object = $response | ConvertFrom-Json
        $number_of_documents = $document_object.Count
    
        for ($i=0; $i -lt $number_of_documents; ++$i)
        {
          $number_of_files = $file_urls.Add($document_object[$i].url)
          $number_of_files = $file_names.Add($document_object[$i].name)
        }
        ++$current_page
        break
      }
      # Too many requests. Pause for 15 seconds
      ElseIf($response.StatusCode -eq 429)
      {
        Write-Host "Too many requests..."
        Start-Sleep -s 15
      }
      # No more files
      ElseIf($response.StatusCode -eq 204)
      {
        Write-Host "No file..."
        $continue = 0
        
      }
    
    }While($continue)

    $number_of_files = $file_names.Count
    Write-Host "..." $number_of_files "files"
    $n = $file_names | Select-Object -Unique

    For ($i=0; $i -lt $number_of_files; ++$i)
    {
      $document_url = $file_urls[$i]
      $document_name = $file_names[$i]
      $output_file = $output_directory + $document_name
  
      $print_string = "(" + ($i+1) + "/" + $number_of_files + ") Downloading: " + $document_name
      Write-Host $print_string
  
      $temp_file = $output_file
      $file_num = 1
      While (Test-Path $temp_file)
      {
        $temp_file = $output_directory + (Get-Item $output_file).BaseName + "($file_num)" + (Get-Item $output_file).Extension
        ++$file_num
      }
      $output_file = $temp_file
 
      # Download the file
      Write-Host $document_url
      #$web_client.DownloadFile($document_url, $output_file)
  
      #slower alternative
      $response = Invoke-WebRequest $document_url -Headers $headers -OutFile $output_file

      

    
     } Write-Host "_____" }
    #download url
    # https://eitacies.assembla.com/spaces/cvnY20b-4r677ccP_HzTya/documents/aNwmtidvGr64XrbQarZsNG/download/aNwmtidvGr64XrbQarZsNG

    # Done
    #[System.Media.SystemSounds]::Asterisk.Play()
    #Write-Host "Press any key to continue ..."
    #$x = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
