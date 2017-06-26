
$AlexiaRand = Get-Random -minimum 0 -Maximum 5
    #Random page from tabified list, 25 links per page
$Rand25 = Get-Random -minimum 1 -Maximum 25
    #Randon link from those identified, 1-25
$itemc = 0
    #clear vars

$WaitSeconds = 240
    #how long to wait for the page to load and sit idle

#$Site = "http://www.alexa.com/topsites/global;" + $AlexiaRand
$Site = "http://www.alexa.com/topsites/category;" + $AlexiaRand +"/Top/Business/"
    #Set the URL to find URLs from

Write-Output "Chose Random URL capture URL: $Site"
Write-Output "Chose Random Link no $Rand25"

$Test = Invoke-WebRequest -usebasicparsing -URI $Site 
    #open the URL and look for valid URLs inside of it

$Test.Links | Foreach {

    $LinkString = $_.href
    $LinkLen = $LinkString.Length

    if ($LinkString -like '*siteinfo*'-AND $LinkLen -gt 10)
        {
        $itemc = $itemc + 1
        $LinkString2 = $LinkString -replace "/siteinfo/","http://www."
        
        if ($itemc -eq $Rand25 )
            {
            $LinkFinal = $LinkString2
            Write-Output "Identified chosen link: $LinkFinal" 
           }

    }
}

Write-Output "Launching URL and closing $waitSeconds seconds later..."
$IE=new-object -com internetexplorer.application
$IE.navigate2($LinkFinal)
$IE.visible=$true

Start-Sleep -s $waitSeconds


Write-Output "Kill the process"
get-process iexplore | stop-process -Force
