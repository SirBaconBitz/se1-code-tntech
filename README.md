# GitLab Population Script

This repo will help you populate a set of GitLab groups for Software Engineering I. This README will guide you through the process.

## Included Files

There a three files included in this repository:

1. README
2. Example CSV with required formatting
3. Python script for population of GitLab

## Setup

### Data Acquisition

The CSV for your class can be extracted via iLearn. The provided CSV is to be used as an example for formatting your own CSV, so make sure to use your CSV when the time comes. Navigate to the class page, then go to Social, then Groups. View the group list for the project groups (NOT the lab groups). There should be an option somewhere within that webpage to export the groups to a CSV file. The group numbers in Column B may need to be filled in manually but should not be hard to do. Place the resulting CSV file in the same folder as your script. This file will be one of your command arguments.

### GitLab Setup

In GitLab, create a parent group to house the different student subgroups that the script will create. Give yourself and your professor(s) Owner level access to ensure you are added as owners in all subgroups. Make note of the parent group ID number; this will be used as one of your command arguments to ensure the subgroups are properly created.

Continuing in GitLab, you will need to create a personal access token. To do this, click on your avatar in the top-right corner, then select Edit Profile. Next, select Access Tokens from the sidebar on the left. You can then enter a token name and expiration date, as well as the scope of the token. Give it full access to ensure no issues arise. Create the token and hold onto this as another argument of the command. For the official guide, visit https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html. 

### Running The Script

Now that you have all of the arguments necessary to run this script, open a command prompt or terminal (depending on OS). Ensure you have Python installed. You will also need to install the gitlab package using pip. The command is as follows:

`pip install gitlab`

Once the necessary package(s) are installed, run the following command to initialize and populate the GitLab subgroups:

`python create_groups_s21.py <csv_file> <parent_id> <token>`

For students to be added to their respective groups, they have to have logged in to GitLab at least once. The first time you run this script, it is likely that not all students will have done this. The command prompt/terminal will leave a message similar to the following:

`<student> was not added to <subgroup> (may already be a member)`

Once more students have joined GitLab, run the script again. The same message will appear more abundantly than the first time, but don't worry. The message appears for both students who haven't joined GitLab AND students who have already been placed in their subgroups. You can run this script as many times as necessary to ensure that all students are placed in their groups.