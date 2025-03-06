# ClockifyPlus
Automated timesheet submission using Clockify API

# How to use!
1. In Clockify go to Preferences (click on your profile picture on the right), then ADVANCED tab and generate your API key. It's sensitive information - keep it secure! 
2. Having the API Key - paste it in the get_workspace_id.sh and run it. You might be required to run "chmod +x get_workspace_id.sh" first for the script to be executable.
3. Copy your Workspace ID - it will be the first ID visible in the output of the script.
4. Now include both API Key and Workspace ID in fill_up_timesheets.py
5. Fill up your timesheet.csv following the defined structure. Keep in mind it's a COMMA separated value file - any additional coma will cause the script to fail reading the file properly.
6. One everything is ready - launch the script!
7. Finally - go to Clockify to make sure every entry has been made correctly. 