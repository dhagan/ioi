#!/usr/bin/perl

################################################################################
#
#       File Name: utilities.cgi
#
#       Purpose: This file is used for 
#
#       Copyright © 2005 IOIntegration Inc. Internal use only.
#
#       Revision History:
#
#       Date            Author          Action
#       ----            ------          ------
#       ??/??/2005      M. Smith        Created this file
#
################################################################################

use CGI qw(:standard escapeHTML);
use CGI::Carp "fatalsToBrowser";
use CGI;
$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";
$cgi = new CGI;
print $cgi->header();
if (param('upload'))
{
	up();
}
elsif (param('download'))
{
	download();
}
elsif (param('uploadRes'))
{
	uploadRes();
}
elsif (param('downloadRes'))
{
	downloadRes()
}
elsif (param('delete'))
{
	deleteFile();
}
elsif (param('newlink'))
{
	newLink();
}
elsif (param('newlinkres'))
{
	newLinkRes();
}
elsif (param('update'))
{
	update();
}
elsif (param('updateres'))
{
	updateRes();
}
elsif (param('loginSearch'))
{
	loginSearch();
}
elsif (param('loginSearchRes'))
{
	loginSearchRes();
}
elsif (param('loginNew'))
{
	loginNew();
}
elsif (param('loginNewRes'))
{
	loginNewRes();
}
else
{
	utilities();
}

sub up()
{
		
	headers();
	background();
	bodyAndLoad();
	print "<FORM ACTION=\"utilities.cgi\" METHOD=\"POST\" ENCTYPE=\"multipart/form-data\">";
	tableHead();
	print "<input type='hidden' name='uploadRes' value='yes'>
		   <tr><td>Name:</td><td><input type='text' name='name'></td></tr>
		   <tr><td>Description:</td><td><input type='text' name='description'></tr>
		   <tr><td>Serial Number</td><td><input type='text' name='serial'</td></tr>
		   <tr><td>File:</td><td><input type='file' name='file'</td></tr>
		   <tr><td colspan = '2'>Allow Customer to download <input type='checkbox' name='allow_cust' default ='No' value='1'></td></tr>
		  	<tr><td colspan='2'><div align='center'><input type='submit' name='submit' value='Submit'></td></tr>
		  </table><center><font color='#808080'><strong>Please try and upload in some kind of stuffed format</font></center></form></body>";
	end_HTML();
}

sub uploadRes()
{
	headers();
	background();
	bodyAndLoad();
	$uploadPath = "/Library/WebServer/dashboard/utilities";
	$fh = param('file');
	$newfh = $fh;
	$newfh =~ s/ /_/g;
	$name = param('name');
	$serial = param('serial');
	$allow_submit = param('allow_cust');
	$description = param('description');
	$size = $ENV{'CONTENT_LENGTH'};
	$statement = "select utility_filename from utilities where utility_filename = '$fh'";
	$duplicate = checkValue($statement);
	if ($duplicate == 0)
	{
		open UPLOADFILE, ">$uploadPath/$newfh";
	
		binmode UPLOADFILE; 
		while ( <$fh> ) 
		{ 
		print UPLOADFILE; 
		} 
		close UPLOADFILE;
		$id_num = selectValues('select max(utility_num) from utilities');
		$id_num++;
		if ($allow_submit eq ""){$allow_submit = "0";}
		insert("insert into utilities (utility_num,utility_name,utility_description,utility_allow_cust,utility_serial,utility_filename,utility_size)
		values ($id_num,'$name','$description',$allow_submit,'$serial','$newfh','$size')");
		print "<center><font color='#808080'>Your upload was successful. Click <a href='utilities.cgi?upload=yes'>here </a> to go back to the upload page.</font>";
	}
	elsif ($duplicate == 1)
	{
		print "<center><font color='#808080'>This file is already available for download, if you wish to replace this file please delete it from the <a href='utilities.cgi?download=yes'>downloads</a> section first.</font></center>";
	}
	end_html();
}
sub download()
{
	headers();
	background();
	bodyAndLoad();
	print "<center><font color = '#808080'><b>IOI Downloads and utilities</b></font></center>";
	tableHead('80%');
	print "<tr><td>File</td><td>Name</td><td>Description</td><td>Size</td><td>Serial #</td><td>Allow Customer</td><td>Update</td><td>Delete</td></tr>";
	utilitiesTable("select utility_filename,utility_name,utility_description,utility_size,utility_serial,utility_allow_cust from utilities order by utility_name");
	print "</table>";
	end_html;
}
sub update()
{
	$filename = param('filename');
	($name,$desc,$serial,$allow_cust) = selectValues("select utility_name,utility_description,utility_serial,utility_allow_cust from utilities where utility_filename = '$filename'");
	headers();
	background();
	bodyAndLoad();
	tableHead('50%');
	print "<form action='' name='form1' id='form1' method='post'>
		   <input type='hidden' name='updateres' value='yes'>
		   <input type='hidden' name='filename' value='$filename'>
		   <tr><td>Name</td><td><input type='text' name='name' value='$name'></td></tr>
		   <tr><td>Description</td><td><input type='text' name='description' value='$desc'></td></tr>
		   <tr><td>Serial</td><td><input type='text' name='serial' value='$serial'></td></tr>
		   <tr><td>Allow Customer</td><td>";
		   print "<input type='checkbox' name='allow_cust' value='Yes' checked>" if ($allow_cust == 1);
		   print "<input type='checkbox' name='allow_cust' value='Yes'>" if ($allow_cust == 0);
		   print "</td></tr><tr><td colspan='2'><div align='center'><input type='submit' name='submit' value='Update'></div></td></tr></form></table>";
		   end_html();
}
sub updateRes
{
	$name= param('name');
	$desc = param('description');
	$serial = param('serial');
	$allow_cust = param('allow_cust');
	$filename = param('filename');
	$desc = quoteValues($desc);
	$serial = quoteValues($serial);
	$name = quoteValues($name);
	if ($allow_cust eq "") {
          $allow_cust = "0";
        } else {
          $allow_cust = "1";}
	insert("update utilities set utility_name=$name,utility_description=$desc,utility_serial=$serial,utility_allow_cust = $allow_cust where utility_filename = '$filename'");
	headers();
	background();
	bodyAndLoad();
	ioiFont("$name has been updated, click <a href='utilities.cgi?download=yes'>here</a> to go back to the downloads page");
	end_html();
}
	
sub deleteFile()
{
	headers();
	background();
	bodyAndLoad();
	$file = param('filename');
	sqlDelete("delete from utilities where utility_filename = '$file'");
	unlink("/Library/WebServer/dashboard/utilities/$file");
	print "<center><font color = '#808080'>'$file' has been deleted sucessfully, click <a href ='utilities.cgi?download=yes'>here</a> to return to the download page.</font></center>";
	end_html();
}
sub utilities()
{
	### DJH $user = $ENV{"REMOTE_USER"};
	### DJH $user =~ s/IOINTEGRATION\\//g;
        $user = getRemoteUser();
	headers();
	background();
	bodyAndLoad();
	print "<div align='center'><font color='#808080' align='center'>My Favorite Links</font><p>";
	tableHead('60%');
	print "<tr><td>Link</td><td>Description</td></tr>";
	staffLinks($user);
	print "</table>";
	print "<p><a href='utilities.cgi?newlink=true&user=$user'>Add New Link</a><p><font color ='#808080'>Other IOI links</font>";
	tableHead('60%');
	print "<tr><td>Link</td><td>Description</td></tr>";
	allLinks($user);
	print "</table>";
	end_html();
}
sub newLink()
{
	### DJH $user = param('user');
        $user = getRemoteUser();
	headers();
	print "<script language='javascript'>
	function submitCheck()
	{
		if (document.form1.link.value == '')
		{
			alert('Please enter a link');
			return false;
		}
		if (document.form1.link_description.value =='')
		{
			alert('Please enter a description');
			return false;
		}
		if (document.form1.file.value == '')
		{
			alert('Please select a file to upload');
			return false;
		}
	}
	</script>";
	background();
	bodyAndLoad();
	tableHead('50%');
	print "<form name='form1' action='utilities.cgi' method='get' onSubmit ='return submitCheck()'>
			<input type='hidden' name='user' value='$user'>
			<input type='hidden' name='newlinkres' value='yes'>
			<tr><td>Link</td><td>http://<input type='text' name='link'></td></tr>
			<tr><td>Description</td><td><input type='text' name='link_description'></td></tr>
			<tr><td colspan ='2'><div align='center'><input type='submit' name='submit' value='Submit'></div></td></tr>
			</table></form>";
	end_html();
}
sub newLinkRes()
{
	headers();
	background();
	bodyAndLoad();
	### DJH $user = param('user');
	$user = getRemoteUser();
	$sa_links = selectValues("select sa_links from staff where sa_login like '$user'");
	$link = param('link');
	$link_description = param('link_description');
	$link_description =~ s/'//g;
	$submit_value = $sa_links . "http://" . $link . "," . $link_description . ";";
	insert("update staff set sa_links = '$submit_value' where sa_login = '$user'");
	print "<div align='center'><font color='#808080'>Link has been successfully added</font><p>
			<a href='utilities.cgi?newlink=true&user=$user'>Create New Link</a><p>
			<a href='utilities.cgi'>Go to my links</a>";
	end_html();
}
sub loginSearch()
{
	headers();
	background();
	bodyAndLoad();
	ioiFont("Please select a company to add/view login information");
	tableHead('50%');
	print "<form name='form1' action='' method='post'>
	<tr><td>Company</td><td>";
	companyDropDown();
	print "</td></tr><tr><td colspan='2'><div align='center'><input type='submit' name='loginSearchRes' value='Go'></form></div></td></tr></table>";
}
sub loginSearchRes()
{
	headers();
	background();
	bodyAndLoad();
	if (param('Edit'))
	{
		$login_username=param('username');
		$id = param('login_id');
		$login_password = param('password');
		$server_ip = param('server_ip');
		$server_name= param('server_name');
		$notes = param('notes');
		$notes = quoteValues($notes);
		$login_username= quoteValues($login_username);
		$login_password = quoteValues($login_password);
		$server_ip = quoteValues($server_ip);
		$server_name= quoteValues($server_name);
		$statement = "UPDATE logins SET login_username=$login_username,login_password=$login_password,login_notes=$notes,login_server_name=$server_name,login_server_ip=$server_ip where login_id='$id'";
		insert($statement);
	}
	
	$company = param('company');
	$dbh = getDBConnection();
	$sth = $dbh->prepare("SELECT login_server_name,login_server_ip,login_username,login_password,login_notes,login_id FROM logins WHERE login_comp_link = '$company'");
	$sth->execute();
	tableHead('75%');
	print "<tr><td>Server Name</td><td>Server IP</td><td>Username</td><td>Password</td><td>Notes</td><td>Edit</td></tr>";
	while (($server_name,$server_ip,$username,$password,$notes,$login_id) = $sth->fetchrow_array())
	{
		print "<tr><td><form name='form1' action='' method='post'>
		<input type='hidden' name='company' value='$company'>
		<input type='hidden' name='loginSearchRes' value='yes'>
		<input type='hidden' name='login_id' value='$login_id'>
		<input type='text' name='server_name' value='$server_name'>
		</td><td><input type='text' name='server_ip' value='$server_ip'></td>
		<td><input type='text' name='username' value='$username'></td>
		<td><input type='text' name='password' value='$password'>
		</td><td><textarea name='notes' rows='5' cols='30'>$notes</textarea></td><td><input type='submit' name='Edit' value='Update'></form></td></tr>";
		
	}
	print "</table><div align='center'><a href='utilities.cgi?loginNew=yes&company=$company'>Create New login</a></div>";

}

sub loginNew()
{
	$company = param('company');
	$comp_name = selectValues("SELECT comp_name FROM company WHERE comp_case_num = '$company'");
	headers();
	print "<script language='javascript'>
	function checkSubmit()
	{
		if (document.form1.server_name.value == '')
		{
			alert(\"Please enter a name to identify this server\");
			return false;
		}
		return true;
	}
	</script>";
		
	background();
	bodyAndLoad();
	ioiFont("Create new login for $comp_name");
	tableHead('50%');
	print "<form name='form1' action ='' method='post' onSubmit='return checkSubmit()'>
	<input type='hidden' name='company' value='$company'>
	<tr><td>Server Name</td><td><input type='text' name='server_name'></td></tr>
	<tr><td>Server IP</td><td><input type='text' name='server_ip'></td></tr>
	<tr><td>Username</td><td><input type='text' name='login_username'></td></tr>
	<tr><td>Password</td><td><input type='text' name='login_password'></td></tr>
	<tr><td>Notes</td><td><textarea name='notes' rows='5' cols='30'></textarea></td></tr>
	<tr><td colspan ='2'><div align='center'><input type='submit' name='loginNewRes' value='Submit'></div></td></tr></table></form>";
}
sub loginNewRes()
{
	$company = param('company');
	$name = param('server_name');
	$ip = param('server_ip');
	$login_username = param('login_username');
	$login_password = param('login_password');
	$notes = param('notes');
	headers();
	background();
	bodyAndLoad();
	$name = quoteValues($name);
	$ip = quoteValues($ip);
	$login_username = quoteValues($login_username);
	$login_password = quoteValues($login_password);
	$notes = quoteValues($notes);
	insert("INSERT INTO logins (login_username,login_password,login_server_name,login_server_ip,login_notes,login_comp_link) 
	values ($login_username,$login_password,$name,$ip,$notes,'$company')");
	ioiFont("Your new login information has been successfully been created.<p><a href='utilities.cgi?loginSearchRes=yes&company=$company'>Go back to this companies logins</a>");
	end_HTML;
}
	

	
	
	
