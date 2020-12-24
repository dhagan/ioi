#!/usr/bin/perl

################################################################################
#
#       File Name: management.cgi
#
#       Purpose: This file is used for updating products,companies and staff
#                members in the database.
#
#       Copyright © 2005 IOIntegration Inc. Internal use only.
#
#       Revision History:
#
#       Date            Author          Action
#       ----            ------          ------
#       08/24/2005      M. Smith        Created this file
#       01/30/0007      B. Scarborough  Updated compUpdate() and compUpdateRes() to
#                                       allow support for company sales and company tech
#       02/09/2007      B. Scarborough  Modified to insure lowercase emails in DB
#       02/22/2007      B. Scarborough  Modified manageReaderPrefs to allow for update of attachments dir
#                                       and accurate representation of EmailReader running or not
#       02/27/2007      B. Scarborough  Modified prodUpdate() to remove checks on OS, version, and options
#       02/27/2007      B. Scarborough  Modified compUpdate() to make comp_tech & comp_sales select from staff
#       03/14/2007      B. Scarborough  Modified compUdate(), compUpdateRes(), contactUpdate(), contactUpdateRes()
#                                       to allow for preferences regarding ticket activity emails
#       04/06/2007      B. Scarborough  Modified compUpdate() to allow for comp_sales and comp_tech options
#                                       to be filtered by department
#       04/20/2007      B. Scarborough  Modified compUpdate() to allow for selectable company organization
################################################################################

use CGI qw(:standard escapeHTML);
use CGI::Carp "fatalsToBrowser";
use CGI;
use Proc::PidUtil qw(:all);
$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";
$cgi = new CGI;
### DJH $user = $ENV{"REMOTE_USER"};
### DJH $user =~ s/IOINTEGRATION\\//g;
$user = getRemoteUser();
$statement = "select sa_permissions from staff where sa_login like '$user'";
$privelages = selectValues($statement);
if (param('product'))
{
	prodUpdate() if (param('product') eq "update");
	prodUpdateRes() if (param('product') eq "updateRes");
	prodSearch() if (param('product') eq "select");
	prodDelete() if (param('product') eq "delete");
}
elsif (param('contact'))
{
	contactCreate() if (param('contact') eq "create");
	contactUpdate() if (param('contact') eq "update");
	contactUpdateRes() if (param('contact') eq "updateRes");
	contactCreateRes() if (param('contact') eq "createRes");
	contactSearch() if (param('contact') eq "select");
	deleteContact() if (param('contact') eq "delete");
}
elsif (param('companystate'))
{
	compSearchOrUpdate() if (param('companystate') eq "select");
	compUpdate() if (param('companystate') eq "update");
	compUpdateRes() if (param('companystate') eq "updateRes");
}
elsif (param('staff'))
{
	staffCreate() if (param('staff') eq "create");
	staffUpdate() if (param('staff') eq "update");
	staffUpdateRes() if (param('staff') eq "updateRes");
	staffCreateRes() if (param('staff') eq "createRes");
}
elsif (param('field'))
{
	fieldCreate() if (param('field') eq "create");
	fieldUpdate() if (param('field') eq "update");
	fieldUpdateRes() if (param('field') eq "updateRes");
	fieldCreateRes() if (param('field') eq "createRes");
}
elsif (param('contract'))
{
	contractCreate() if (param('contract') eq "create");
	contractCreate() if (param('contract') eq "update");
	contractUpdateRes() if (param('contract') eq "updateRes");
	contractCreateRes() if (param('contract') eq "createRes");
}
elsif (param('manageReader'))
{
	manageReader() if (param('manageReader') eq "manage");
	manageReaderRes() if (param('manageReader') eq "manageRes");
}
elsif (param('manageUsers')) {
	manageUsers() if (param('manageUsers') eq "yes");
	deleteUser() if (param('manageUsers') eq "delete");
	deleteUserRes() if (param('manageUsers') eq "deleteUserRes");
	modifyUser() if (param('manageUsers') eq "modify");
	modifyUserRes() if (param('manageUsers') eq "modifyUserRes");
}
elsif (param('emailReader'))
{
	emailReaderOptions();
}
else 
{
	selectAction();
}

sub selectAction()
{
	print $cgi->header();
	headers();
	print "<script language='javascript'>
	function compUpdate()
	{
		if (document.compform.company.value != '')
		{
			document.compform.action = '';
			document.compform.companystate.value = 'update';
			document.compform.submit();
			return true;
		}
		else
		{
			alert('Please select a company to update');
			return false;
		}
	}
	function compCreate()
	{
		document.compform.action= '/companySubmit.html';
		document.compform.submit();
		return true;
	}
	function prodUpdate()
	{
		if (document.prodform.company.value != '')
		{
			document.prodform.action = '';
			document.prodform.product.value = 'select';
			document.prodform.submit();
			return true;
		}
		else
		{
			alert('Please select  a company to update products for');
			return false;
		}
	
	}
	function prodCreate()
	{
		if (document.prodform.company.value != '')
		{
			document.prodform.action = 'productSubmit.cgi';
			document.prodform.comp_case_num.value= document.prodform.company.value;
			document.prodform.submit();
			return true;
		}
		else 
		{
			alert('Please select a company to create a new product for');
			return false;
		}
	}
	function contactUpdate()
	{
		if (document.contactform.company.value != '')
		{
			document.contactform.action = '';
			document.contactform.contact.value = 'select';
			document.contactform.submit();
			return true;
		}
		else 
		{
			alert('Please select a company in order to update their contacts');
			return false;
		}
	}
	function contactCreate()
	{
		if (document.contactform.company.value != '')
		{
			document.contactform.action = 'customerSubmit.cgi';
			document.contactform.contact.value='create';
			document.contactform.submit();
			return true;
		}
		else
		{
			alert('Please select a company to create a contact for');
			return false;
		}
	}

	function contractUpdate()
	{
		if (document.contractform.company.value != '')
		{
			document.contractform.action = '';
			document.contractform.contract.value='create';
			document.contractform.submit();
			return true;
		}
		else
		{
		alert('Please select a company to create a contract for');
		return false;
		}
	}		
			
	function staffUpdate()
	{
		if (document.staffform.staff.assigned_to.value != '')
		{
			document.staffform.action= '';
			document.staffform.staff.value = 'update';
			document.staffform.submit();
			return true;
		}
		else
		{
			alert('Please select a staff member to update');
			return false;
		}
	}
	function staffCreate()
	{
			document.staffform.action = '';
			document.staffform.staff.value='create';
			document.staffform.submit();
			return true;
	}
	function staffUpdate()
	{
		if (document.staffform.assigned_to.value != '')
		{
			document.staffform.action = '';
			document.staffform.staff.value = 'update';
			document.staffform.submit();
			return true;
		}
	}
	function fieldUpdate()
	{
		if (document.fieldform.dynamic_field.value != '')
		{
			document.fieldform.action = '';
			document.fieldform.field.value = 'update';
			document.fieldform.submit();
			return true;
		}
		else
		{
			alert('Please select a field to update');
			return false;
		}
	}
	function fieldCreate()
	{
			document.fieldform.action = '';
			document.fieldform.staff.value='create';
			document.fieldform.submit();
			return true;
	}
		
	
	</script>";
	bodyAndLoad();
	background();
	tableHead('70%');
	print "<tr><td colspan = '3'><div align='center'><b>Dashboard Management</b></div></td></tr>
		   <tr><form name='compform' id='compform' onsubmit='return compCheck();'>
		   <input type='hidden' name='companystate'>
		   <td>Company</td><td>";
		   companyDropDown();
	print "&nbsp;&nbsp;<input type='submit' name='update' value='Update Company' onClick ='return compUpdate();'></td>
		   <td><input type='submit' name='Submit' value='Create New Company' onclick='return compCreate();'></td></form></tr>
		   <tr><form name='prodform' id='prodpform' onsubmit='return prodCheck();'>
		   <input type='hidden' name='product'>
		   <input type='hidden' name='comp_case_num'>
		   <td>Product</td>
		   <td>";
		   companyDropDown();
	print "&nbsp;&nbsp;<input type ='submit' name='submit' value='Update Products' onClick='return prodUpdate();'></td>
		  <td><input type='submit' name='submit' value='Create New Product' onClick='return prodCreate();'></form></td></tr>
		  <tr><form name='contactform' id='contactform' onsubmit='return contactCheck();'>
		  <input type='hidden' name='contact'>
		  <td>Contacts</td><td>";
		  companyDropDown();
	print "&nbsp;&nbsp;<input type ='submit' name='submit' value='Update Contacts' onClick=' return contactUpdate();'></td>
		  <td><input type='submit' name='submit' value='Create New Contact' onClick='return contactCreate();'></td></form></tr>";
	print "<tr><form name='contractform' id='contractform'>
			<input type='hidden' name='contract'>
			<td>Contracts</td><td>";
			companyDropDown();
	print "&nbsp;&nbsp;<input type='submit' name='submit' value='Update Contracts' onClick = 'return contractUpdate()'></td>
		   <td></td></form></tr>";
	if ($privelages eq "admin")
	{
	
		print "<tr><form name='staffform' id='staffform' onsubmit='return contactCheck();'>
		  <input type='hidden' name='staff'>
		  <td>Staff</td><td>";
		  staffDropDown("assigned_to", "true");
   		print "&nbsp;&nbsp;<input type ='submit' name='submit' value='Update Staff' onClick='return staffUpdate();'></td>
   		  <td><input type='submit' name='submit' value='Create New Staff' onClick='return staffCreate();'></td></form></tr>
   		   <tr><form name='fieldform' id='fieldform' onsubmit='return fieldCheck();'>
   		   <input type='hidden' name='field'>
   		  <td>Field</td><td>";
   		  fieldDropDown();
   		print "</td><td><input type='submit' name='submit' value='Update Field' onclick='return fieldUpdate();'></form>";
   		print "</tr></tr><td colspan='3'><div align='center'><form name='emailreader' action='' id='emailreader'>
   		<input type='hidden' name='emailReader' value='yes'>
   		<input type='submit' name='submit' value='Email Reader Options'></div></td></tr>
		<tr><td colspan='3'><div align='center'><a href='management.cgi?manageUsers=yes'>Manage Users</a></form>";
   	}
   	print"</table>";
   	end_HTML();
}
sub contractCreate()
{
	$comp_case_num = param('company');
	($comp_name) = selectValues("SELECT comp_name FROM company WHERE comp_case_num = '$comp_case_num'");
	($contract_comp_link,$contract_type,$contract_date_created,$contract_date_expired,$contract_status,$contract_notes) = selectValues("SELECT contract_comp_link,contract_type,contract_date_created,contract_date_expired,contract_status,contract_notes FROM contract WHERE contract_comp_link = '$comp_case_num'");
	@pur_date = split(/-/,$contract_date_created);
	@exp_date = split(/-/,$contract_date_expired);
	print $cgi->header();
	headers();
	print "<script language='javascript'>
	function checkSubmit()
	{
		if (document.form1.ioi_support.value = '')
		{
			alert('Please choose the IOI Support type');
			return false;
		}
		else if (document.form1.yearcontract.value ='' || document.form1.monthcontract.value = '' || document.form1.daycontract.value = '')
		{
			alert('Please choose the date purchased');
			return false;
		}
		else if (document.form1.yearcontract_exp.value = '' || document.form1.monthcontract_exp.value = '' || document.form1.daycontract_exp.value ='')
		{
			alert('Please choose the date expired');
			return false;
		}
		return true;
	}
	</script>";
	menu_focus();
	background();
	bodyAndLoad("menu_focus(document.form1.ioi_support,\"$contract_type\");menu_focus(document.form1.yearcontract,\"@pur_date[0]\");menu_focus(document.form1.monthcontract,\"@pur_date[1]\");
	menu_focus(document.form1.daycontract,\"@pur_date[2]\");menu_focus(document.form1.yearcontract_exp,\"@exp_date[0]\");menu_focus(document.form1.monthcontract_exp,\"@exp_date[1]\");
	menu_focus(document.form1.daycontract_exp,\"@exp_date[2]\");");
	ioiFont("Edit contract for $comp_name");
	tableHead('70%');
	print "<form name='form1' action='management.cgi' method='post' onSubmit='return checkSubmit();'>
	<input type='hidden' name='contract' value='createRes'>
	<input type='hidden' name='comp_case_num' value='$comp_case_num'>";
	print "<tr><td>Support Level</td><td>";
	dynamicDropDown('ioi_support','','ioi_support');
	print "</td></tr><tr><td>Date Purchased</td><td>";
	dateDropDown('contract','contract','contract');
	print "</td></tr><tr><td>Date Expires</td><td>";
	dateDropDown('contract_exp','contract_exp','contract_exp');
	print "</td></tr><tr><td>Notes</td><td><textarea name='notes' rows='10' cols ='50'>$contract_notes</textarea></tr>
	<tr><td colspan='2'><div align='center'><input type='submit' name='Update' value='Update'></div></td></tr>
	</table>
	</form>";
	end_HTML;
}
sub contractCreateRes()
{
	$comp_case_num = param('comp_case_num');
	$year_created = param('yearcontract');
	$month_created = param('monthcontract');
	$day_created = param('daycontract');
	$year_exp = param('yearcontract_exp');
	$month_exp = param('monthcontract_exp');
	$day_exp = param('daycontract_exp');
	$contract_type = param('ioi_support');
	$contract_notes = param('notes');
	$contract_notes = quoteValues($contract_notes);
	$contract_num = selectValues("SELECT contract_num from contract where contract_comp_link = '$comp_case_num'");
	$date_created = $year_created . "-" . $month_created . "-" . $day_created;
	$date_exp = $year_exp . "-" . $month_exp . "-" . $day_exp;
	print $cgi->header();
	insert("UPDATE contract SET contract_type='$contract_type', contract_notes=$contract_notes, contract_date_created='$date_created', contract_date_expired='$date_exp' where contract_comp_link='$comp_case_num'") if ($contract_num ne "");
	insert("INSERT INTO contract (contract_type,contract_date_created,contract_date_expired,contract_notes, contract_comp_link) VALUES ('$contract_type','$date_created','$date_exp',$contract_notes,'$comp_case_num')") if ($contract_num eq "");
	headers();
	background();
	ioiFont("Contract updated successfully.<p>Back to the <a href='management.cgi'>management</a> page");
	end_HTML;
}

sub fieldUpdate()
{
	$thisField = param('dynamic_field');
	($field_name,$field_title,$field_data) = selectValues("select field_name,field_title,field_data from dynamic_fields where field_name = '$thisField'");
	print $cgi->header();
	headers();
	background();
	bodyAndLoad();
	tableHead('65%');
	print "<form name='form1' id='form1' action = '' method='get'>
			<input type='hidden' name='field_name' value='$field_name'>
			<input type='hidden' name='field_title' value='$field_title'>
			<input type='hidden' name='field' value='updateRes'>
		   <tr><td><div align='center'><b>Update Data for '$field_title' field</b></div></td></tr>
		   <tr><td><div align='center'>Data</div></td></tr>
		   <tr><td><div align='center'>Put a ';' before each main value.<p><textarea name='field_data' rows='20' cols='40'>$field_data</textarea></div></td></tr>
		   <tr><td><div align='center'><input type='submit' name='submit' value='Update $field_title Field'></td></tr>
		   </form>
		   </table>";
	end_html();
}
sub fieldUpdateRes()	
{
	$field_name = param('field_name');
	$field_data = param('field_data');
	$field_title = param('field_title');
	print $cgi->header();
	insert("update dynamic_fields set field_data = '$field_data' where field_name = '$field_name'");
	headers();
	background();
	bodyAndLoad();
	ioiFont("Field '$field_title' has been successfully updated. Click <a href='management.cgi?field=update&dynamic_field=$field_name'>here</a> to modify your recently changed field");
	end_html();
}
# sub createField()
# {
# 	print $cgi->header();
# 	header();
# 	background();
# 	body();
# 	tableHead('65%');
# 	print "<form name='form1' id='form1' action ='' method='post'>
# 		   <input type='hidden' name='field' value='createRes'>
# 		   <tr><td colspan='2'><div align='center'><b>Create Field</b></div></td></tr>
# 		   <tr><td>Field Name (cannot include space)</td><td><input type='text' name='field_name'></td></tr>
# 		   <tr><td>Field Title</td><td><input type='text' name='field_title'></td></tr>
# 		   <tr><td colspan='2'><div align='center'>Field Data</div></td></tr>
# 		   <tr><td colspan='2'><div align='center'><textarea name='field_name' rows='20' cols='40'></textarea></div></td></tr>
# 		   <tr><td colspan='2'><div align='center'><input type='submit' name='submit' value='Create Field'></div></td></tr>
# 		   </form>
# 		   </table>";
# 	end_html();
# }
# sub createFieldRes()
# {

# Function: compUpdate
# Purpose: Displays the page where a company's information is updated
# Inputs: HTML parameters
# Returns: None

sub compUpdate()
{
	$comp_case_num = param('company');
	print $cgi->header();
	($comp_name,$comp_phone,$comp_bill_address,$comp_bill_city,$comp_bill_state,$comp_bill_zip,$comp_fax,$comp_www,$comp_status,$comp_notes,$comp_org,$comp_reg,$comp_email,$comp_sales,$comp_tech,$allow_reports) =
	selectValues("select comp_name,comp_phone,comp_bill_address,comp_bill_city,comp_bill_state,comp_bill_zip,comp_fax,comp_www,comp_status,comp_notes,comp_org,comp_reg,comp_email,comp_sales,comp_tech,allow_reports from company where comp_case_num = '$comp_case_num'");
	if($allow_reports eq 1) {
                $allow_reports = "checked";
        } else {
                $allow_reports = "";
        }
        headers();
	background();
	menu_focus();
	bodyAndLoad("menu_focus(document.form1.comp_status,\"$comp_status\")");
	print "<form action = '' name='form1' id='form1' onSubmit= 'return checkSubmit'>
		   <input type='hidden' name='companystate' value='updateRes'>
		   <input type='hidden' name='comp_case_num' value='$comp_case_num'>";
	
	tableHead('70%');
	print "<tr><td colspan = '2'><div align='center'><b>Update company $comp_name</b></div></td></tr>
		  <tr><td>Company Name</td><td><input type='text' size='30' name='comp_name' value='$comp_name'></td></tr>
		  <tr><td>Company Phone</td><td><input type='text' size='30' name='comp_phone' value='$comp_phone'></td></tr>
		  <tr><td>Company Group Email</td><td><input type='text' size='30' name='comp_email' value='$comp_email'>
		  <tr><td>Company Fax</td><td><input type='text' size='30' name='comp_fax' value='$comp_fax'></td></tr>
		  <tr><td>Billing Address</td><td><input type='text' size='30' name='comp_bill_address' value='$comp_bill_address'></td></tr>
		  <tr><td>Billing City</td><td><input type='text' size='30' name='comp_bill_city' value='$comp_bill_city'></td></tr>
		  <tr><td>Billing State</td><td><input type='text' size='30' name='comp_bill_state' value='$comp_bill_state'></td></tr>
		  <tr><td>Billing Zip</td><td><input type='text' size='30' name='comp_bill_zip' value='$comp_bill_zip'></td></tr>
		  <tr><td>Company WWW</td><td><input type='text' size='30' name='comp_www' value='$comp_www'></td></tr>
		  <tr><td>Company Sales</td><td>";
        staffDropDown("comp_sales", "true", $comp_sales, "Sales");
        print "</td></tr>
                  <tr><td>Company Tech</td><td>";
        staffDropDown("comp_tech", "true", $comp_tech, "IT");
        print "</td></tr>
                  <tr><td>Status</td><td><select name='comp_status' id='comp_status'><option value='Disabled'>Disabled<option value='Active'>Active</select></td></tr>
		  <tr><td>Company Organization</td><td><input type='text' size='30' name='comp_org' value='$comp_org' />&nbsp;&nbsp;<select name='orgSelect' onChange='this.form.comp_org.value=this.value'><option value=''>ADD TO EXISTING:</option>";
        my $dbh = getDBConnection();
        my $sth = $dbh->prepare("SELECT DISTINCT comp_org FROM company WHERE comp_org <> '' ORDER BY comp_org ASC");
	$sth->execute();
        while (my ($org) = $sth->fetchrow_array()) {
                print "<option value='$org'>$org</option>";
        }
        print "</select></td></tr>
		  <tr><td>Company Region</td><td><input type='text' name='comp_reg' size='30' value='$comp_reg'></td></tr>
		  <tr><td>Ticket Activity Report Emails</td><td><input type='checkbox' name='allow_reports' value='allow_reports' $allow_reports></td></tr>
                  <tr><td>Company Notes</td><td><textarea name='comp_notes' rows='5' cols='30'>$comp_notes</textarea></td></tr>
		  <tr><td colspan = '2'><div align='center'><input type='submit' name='submit' value='Update'></div></td></tr>
		  </table>";
        end_html();
        $dbh->disconnect();
}

# Function: compUpdateRes
# Purpose: Updates the DB with a company's new information
# Inputs: HTML parameters
# Returns: None

sub compUpdateRes()
{
	my $comp_case_num = param('comp_case_num');
	my $comp_name = param('comp_name');
	my $comp_phone = param('comp_phone');
	my $comp_fax = param('comp_fax');
	my $comp_email = lc(param('comp_email'));
	my $comp_bill_address = param('comp_bill_address');
	my $comp_bill_city = param('comp_bill_city');
	my $comp_bill_state = param('comp_bill_state');
	my $comp_bill_zip = param('comp_bill_zip');
	my $comp_www = param('comp_www');
	my $comp_status = param('comp_status');
	my $comp_org = param('comp_org');
	my $comp_reg = param('comp_reg');
	my $comp_notes = param('comp_notes');
        my $comp_sales = param('comp_sales');
        my $comp_tech = param('comp_tech');
        my $allow_reports = 0;
        $allow_reports = 1 if (param('allow_reports'));
	$comp_name = quoteValues($comp_name);
	$comp_bill_address = quoteValues($comp_bill_address);
	$comp_bill_city = quoteValues($comp_bill_city);
	$comp_org = quoteValues($comp_org);
	$comp_notes = quoteValues($comp_notes);
	print $cgi->header();
	headers();
	my $statement = "update company set comp_name = $comp_name,comp_phone = '$comp_phone',comp_fax = '$comp_fax',comp_bill_address = $comp_bill_address,comp_bill_city = $comp_bill_city,comp_bill_state='$comp_bill_state',comp_bill_zip ='$comp_bill_zip'
	,comp_www = '$comp_www',comp_status = '$comp_status',comp_org = $comp_org,comp_notes=$comp_notes,comp_email='$comp_email',comp_sales='$comp_sales',comp_tech='$comp_tech', allow_reports = $allow_reports where comp_case_num = '$comp_case_num'";
	insert($statement);

	background();
	bodyAndLoad();
	ioiFont("The company $comp_name has been updated successfully");
	end_html();
}
sub prodDelete()
{
	print header();
	background();
	my $prod_case_num = param('prod_case_num');
	my $dbh = getDBConnection();
	my $statement = "DELETE from product WHERE prod_case_num = '$prod_case_num'";
	$sth = $dbh->prepare($statement);
	$sth->execute();
	$sth->finish();
	$dbh->commit();
	$dbh->disconnect();
	ioiFont("Product deleted successfully");
}
sub prodSearch()
{
	$comp_case_num = param('company');
	my $dbh = getDBConnection();
	$dbh-> {'LongReadLen'} = 1000000;
	$sth = $dbh->prepare("select prod_case_num,prod_name,prod_version,prod_part_num from product where prod_comp_link = '$comp_case_num'");
	$sth->execute();
	print $cgi->header();
	headers();
	print "<script language='javascript'>
	function deleteProd()
	{
		var confirmCheck = confirm('Are you sure you want to delete this product');
		if(confirmCheck)
		{
			return true;
		}
		else
		{
			return false;	
		}
	}
	</script>";
	background();
	bodyAndLoad();
	tableHead('70%');
	print "<tr><td>Product Name</td><td>Serial #</td><td>Version</td><td>Delete</td></tr>";
	while(($prod_case_num,$prod_name,$prod_version,$prod_part_num) = $sth->fetchrow_array())
	{
		print "<form name='form1' action='' method='get' onSubmit='return deleteProd()'>
		<input type='hidden' name='product' value='delete'>
		<input type='hidden' name='prod_case_num' value='$prod_case_num'>
		<tr><td><a href='management.cgi?product=update&prod_case_num=$prod_case_num'>$prod_name</a></td><td>$prod_part_num</td><td>$prod_version</td><td>
		<input type='submit' name='submit' value='Delete' ></form></td></tr>";
	}
	print "</table>";
	end_html();
}
sub prodUpdate()
{
	$prod_case_num = param('prod_case_num');
	($prod_name,$prod_version,$prod_oper_sys,$prod_notes,$prod_part_num,$prod_invoice,$prod_status,$sub_prod_name,$prod_maint_exp,$date_prod_purchased,$tape_slots,$tape_drives) = 
	 selectValues("select prod_name,prod_version,prod_oper_sys,prod_notes,prod_part_num,prod_invoice,prod_status,sub_prod_name,prod_maint_exp,date_prod_purchased,prod_slot_num,prod_drive_num from product where prod_case_num = '$prod_case_num'");
	$date_prod_purchased =~ s/00:00:00//g;
	$prod_maint_exp =~ s/00:00:00//g;
	$prod_version =stripWhitespace($prod_version);
	$prod_oper_sys = stripWhitespace($prod_oper_sys);
	$sub_prod_name = stripWhitespace($sub_prod_name);
	$date_prod_purchased = "Empty" if !($date_prod_purchased);
	$prod_maint_exp = "Empty" if !($prod_maint_exp);
	print $cgi->header();
	headers();
	menu_focus();
	print "<script language ='javascript'>
	function setup()
	{
		menu_focus(document.form1.prod_version,\"$prod_version\");
		menu_focus(document.form1.sub_prod_name,\"$sub_prod_name\");
		menu_focus(document.form1.prod_oper_sys,\"$prod_oper_sys\");
		if (\"Tape Library\" == \"$prod_name\")
		{
			menu_focus(document.form1.tape_slots,\"$tape_slots\");
			menu_focus(document.form1.tape_drives,\"$tape_drives\");
		}
	}
	function checkSubmit()
	{
		var prod_purchased = '$date_prod_purchased';
		var prod_maint_exp = '$prod_maint_exp';
		if (prod_purchased == \"Empty\")
		{  
			if (document.form1.daypurchased.value == '' || document.form1.monthpurchased.value == '' || document.form1.yearpurchased.value == '')
			{
				alert('You must enter a date that this product was purchased');
				return false;
			}
		}
		if (prod_maint_exp == \"Empty\")
		{  
			if (document.form1.daymaint.value == '' || document.form1.monthmaint.value == '' || document.form1.yearmaint.value == '')
			{
				alert('You must enter a date that this products maintenance will expire');
				return false;
			}
		}
			if (document.form1.prod_part_num.value == '')
			{ alert('Product Serial # cannot be empty'); return false; }
		return true;
	}
	</script>";
	background();
	bodyAndLoad('setup()');
	tableHead('70%');
	print "<form name='form1' id='form1' action = '' onsubmit='return checkSubmit()'>
			<input type='hidden' name='product' value='updateRes'>
			<input type='hidden' name='prod_case_num' value='$prod_case_num'>
			<input type='hidden' name='prod_name' value='$prod_name'>
			<tr><td>Product Name</td><td>$prod_name</td></tr>
		   <tr><td>Serial #	</td><td><input type='text' name='prod_part_num' value='$prod_part_num'></td></tr>
		   <tr><td>Version	</td><td>";
		   dynamicDropDown('prod_version',$prod_name,'prod_version');
		   print"</td></tr>
		   <tr><td>Operating System	</td><td>";
		   dynamicDropDown('prod_oper_sys','','prod_oper_sys');
		   print "</td></tr>
		   <tr><td>Options/Model</td><td>";
		   print "Media:" if ($prod_name =~ /Tape/i);
		   dynamicDropDown('sub_prod_name',"$prod_name",'sub_prod_name');
		   if ($prod_name =~ /Tape/i)
		   {
			   print "Slots:";
			   dynamicDropDown('tape_slots','','tape_slots');
			   print "Drives:";
			   dynamicDropDown('tape_drives','','tape_drives');
		   }
		   print "</td><tr><td>Date Purchased</td><td>";
		   dateDropDown('purchased','purchased','purchased');
		   print "(Currently $date_prod_purchased)</td></tr>
		   <tr><td>Maintenance Exp.</td><td>";
		   dateDropDown('maint','maint','maint');
		   print "(Currently $prod_maint_exp)</td></tr>
		   </td></tr>
		   <tr><td>Product Notes</td><td><textarea name='prod_notes' rows='10' cols='60'>$prod_notes</textarea></td></tr>";
		   print "</td></tr><tr><td colspan='2'><div align='center'><input type='submit' name='submit' value='Update $prod_name'></div></td></tr>
		   </form></table>";
	end_html();	   
}
sub prodUpdateRes()
{
	print $cgi->header();
	$prod_name = param('prod_name');
	$prod_case_num = param('prod_case_num');
	$prod_part_num = param('prod_part_num');
	$prod_version = param('prod_version');
	$prod_oper_sys = param('prod_oper_sys');
	$sub_prod_name = param('sub_prod_name');
	$daypurchased = param('daypurchased');
	$monthpurchased = param('monthpurchased');
	$yearpurchased = param('yearpurchased');
	$tape_drives = param('tape_drives');
	$tape_slots = param('tape_slots');
	$date_prod_purchased = $yearpurchased . "-" . $monthpurchased . "-" . $daypurchased if ($daypurchased and $monthpurchased and $yearpurchased);
	$daymaint = param('daymaint');
	$monthmaint = param('monthmaint');
	$yearmaint = param('yearmaint');
	$prod_maint_exp = $yearmaint . "-" . $monthmaint . "-" . $daymaint if ($daymaint and $monthmaint and $yearmaint);
	$prod_notes = param('prod_notes');
	$prod_notes = quoteValues($prod_notes);
	$sub_prod_name = quoteValues($sub_prod_name);
	$prod_version = quoteValues($prod_version);
	$statement = "update product set prod_part_num = '$prod_part_num',prod_version =$prod_version,prod_oper_sys = '$prod_oper_sys',sub_prod_name = $sub_prod_name,prod_notes = $prod_notes,prod_drive_num = '$tape_drives',prod_slot_num = '$tape_slots'";
	$statement = $statement . ",date_prod_purchased = '$date_prod_purchased'" if ($date_prod_purchased);
	$statement = $statement . ",prod_maint_exp = '$prod_maint_exp'" if ($prod_maint_exp);
	$statement = $statement . "where prod_case_num = '$prod_case_num'";
	insert($statement);
	headers();
	background();
	bodyAndLoad();
	ioiFont("$prod_case_num '$prod_name has been successfully updated. Click <a href='management.cgi?prod_case_num=$prod_case_num'>here</a> to modify your recently updated product.<p>
			Click <a href=''>here</a>to go back to the management page.");
	end_html();
}
sub contactSearch()
{
	$comp_case_num = param('company');
	$comp_name = param('comp_name');
	my $dbh = getDBConnection();
	$dbh-> {'LongReadLen'} = 1000000;
	$sth = $dbh->prepare("select comp_name from company where comp_case_num = '$comp_case_num'");
	$sth->execute();
	$comp_name = $sth->fetchrow_array();
	$sth = $dbh->prepare("select sub_login,sub_name,sub_e_mail,sub_phone from users where sub_comp_link = '$comp_case_num'");
	$sth->execute();
	print $cgi->header();
	headers();
	print "<script name='javascript'>
	function checkSubmit(thisUser)
	{
		var confirmDelete = confirm('Are you sure that you want to delete the user ' + thisUser);
		if(confirmDelete)
		{
			return true;
		}
		else
			return false;
	}
	</script>";
	background();
	bodyAndLoad();
	tableHead('70%');
	print "<tr><div align='center'>";
	ioiFont("Contacts for $comp_name");
	print "</div></tr>";
	print "<tr><td>Customer Name</td><td>Email</td><td>Phone</td><td>Delete</td></tr>";
	$i = 0;
	while(($sub_login,$sub_name,$sub_email,$sub_phone) = $sth->fetchrow_array())
	{
		print "<form name='form$i' method='post' onSubmit='return checkSubmit(\"$sub_login\")'>
		<input type='hidden' name='contact' value='delete'>
		<input type='hidden' name='deleteContact' value='$sub_login'>
		<tr><td><a href='management.cgi?contact=update&sub_login=$sub_login'>$sub_name</a></td><td>$sub_email</td><td>$sub_phone</td>
		<td><input type='submit' name='submit' value='Delete'></td></tr>
		</form>";
		$i++;
	}
	print "</table>";
	end_html();
}	
sub deleteContact()
{
	print header();
	background();
	my $login = param('deleteContact');
	my $dbh = getDBConnection();
 	my $sth = $dbh->prepare("DELETE FROM users WHERE sub_login = '$login'");
 	$sth->execute();
 	$dbh->commit();
 	$dbh->disconnect();
	ioiFont("You have successfully deleted the users $login");
}
sub contactUpdate()
{
	$sub_login = param('sub_login');
	$fromUpdate = param('fromUpdate');
	($sub_name,$sub_e_mail,$sub_phone,$sub_notes,$sub_access,$sub_dept,$sub_org,$sub_fax,$sub_cell,$sub_password,$allow_reports) = selectValues("select sub_name,sub_e_mail,sub_phone,sub_notes,sub_access
	,sub_dept,sub_org,sub_fax,cell_phone,sub_password,allow_reports from users where sub_login = '$sub_login'");
	if($allow_reports eq 1) {
                $allow_reports = "checked";
        } else {
                $allow_reports = "";
        }
        print $cgi->header();
	headers();
	background();
	menu_focus();
	print "<script language='javascript'>
 	function setup()
 	{
 		menu_focus(document.form1.sub_access,\"$sub_access\");
 	}
 	function checkSubmit()
 	{
 		if (document.form1.sub_name.value == ''){ alert('Please enter a name for this contact'); return false;}
 		if (document.form1.sub_email.value ==''){alert('Please enter an email for this contact'); return false;}
 		if (document.form1.sub_phone.value ==''){alert('Please enter a phone # for this contact'); return false;}
 		if (document.form1.sub_login.value == ''){alert('Please enter a login for this contact'); return false;}
 		if (document.form1.sub_password.value == ''){alert('Please enter a password for this contact'); return false;}
 		if (document.form1.sub_access.value == 'Disabled'){var checkdisable = confirm('Are you sure you want to disable this account');
 		if (checkdisable == true)
 		{
 		}
 		else
 		{
 			menu_focus(document.form1.sub_access,'Active');
 			return false;
 		}
 		return true;
 		}
 			
 	}
 	</script>";
 	bodyAndLoad('setup();');
 	ioiFont("The login you entered is already in use by another contact") if (param('duplicate_login'));
 	print "<form name='form1' id='form1' action = '' onsubmit='return checkSubmit()'>
 			<input type='hidden' name='old_login' value='$sub_login'>
 			<input type='hidden' name='old_email' value='$sub_e_mail'>
 			<input type='hidden' name='fromUpdate' value='$fromUpdate'>
 			<input type='hidden' name='contact' value='updateRes'>\n";
 	tableHead('50%');
 	print "<tr><div align='center'>Update contact '$sub_name'</div></tr>
 		   <tr><td>Name</td><td><input type='text' name='sub_name' value='$sub_name'></td></tr>
 		   <tr><td>Login</td><td><input type='text' name='sub_login' value='$sub_login'></td></tr>
 		   <tr><td>Password</td><td><input type='text' name='sub_password' value='$sub_password'></td></tr>
 		   <tr><td>Email</td><td><input type='text' name='sub_email' value='$sub_e_mail'></td></tr>
 		   <tr><td>Phone</td><td><input type='text' name='sub_phone' value='$sub_phone'></td></tr>
 		   <tr><td>Cell Phone</td><td><input type='text' name='cell_phone' value='$sub_cell'></td></tr>
 		   <tr><td>Fax</td><td><input type='text' name='sub_fax' value='$sub_fax'></td></tr>
 		   <tr><td>Access</td><td><select name='sub_access'><option value='Active'>Active</option><option value='Disabled'>Disabled</option></select></td></tr>
		   <tr><td>Department</td><td><input type='text' name='sub_dept' value='$sub_dept'></td></tr>
		   <tr><td>Ticket Activity Report Emails</td><td><input type='checkbox' name='allow_reports' value='allow_reports' $allow_reports></td></tr>
                   <tr><td>Notes</td><td><textarea name='sub_notes' rows='10' cols='60'>$sub_notes</textarea></td></tr>
<!-- DJH
		   <tr><td colspan='2'><div align='center'><input type='submit' name='submit' value='Update $sub_name'></div></td></tr>
-->
		   <tr><td colspan='2'><div align='center'>To update use IOIDashboard.</div></td></tr>
		   </table></form>";
	end_HTML();
}
sub contactUpdateRes()
{
	my $dbh = getDBConnection();
	$dbh-> {'LongReadLen'} = 1000000;
	$sub_login = param('sub_login');
	$sub_email = param('sub_email');
	$old_email = param('old_email');
	$old_login =param('old_login');
	$sth = $dbh->prepare("select sub_login from users where sub_login = '$sub_login' and sub_e_mail <> '$old_email'");
	$sth->execute();
	$duplicateValue = $sth->fetchrow_array();
	print $cgi->redirect('management.cgi?sub_login=$old_login&contact=update&duplicate_login=yes') if ($duplicateValue ne "");
	$sub_name = param('sub_name');
	$sub_phone = param('sub_phone');
	$cell_phone = param('cell_phone');
	$sub_fax = param('sub_fax');
	$sub_access = param('sub_access');
	$sub_dept = param('sub_dept');
	$sub_notes = param('sub_notes');
	$sub_password = param('sub_password');
	$sub_notes = quoteValues($sub_notes);
	$sub_email = quoteValues(lc($sub_email));
	$sub_name = quoteValues($sub_name);
        $allow_reports = 0;
        $allow_reports = 1 if (param('allow_reports'));
	insert("update users set sub_name=$sub_name,sub_e_mail=$sub_email,sub_phone='$sub_phone',sub_dept='$sub_dept',sub_notes = $sub_notes,cell_phone='$cell_phone',sub_fax='$sub_fax',
		   sub_access = '$sub_access',sub_password = '$sub_password',allow_reports = $allow_reports where sub_login = '$old_login'");
	print $cgi->header();
	headers();
	background();
	bodyAndLoad();
	ioiFont("'$sub_name' has been updated, click <a href='management.cgi?sub_login=$sub_login&contact=update'>here</a> to modify your recently updated contact.<p>Click <a href=''>here</a> to go back to the management page.") if (param('fromUpdate') ne "Yes");
	ioiFont("'$sub_name' has been updated successfully.<p><input type='button' name='close' value='Close Window'  onClick='javascript:window.close();'>") if (param('fromUpdate') eq "Yes");
	end_html();
}
sub staffUpdate()
{
	print $cgi->header();
	headers();
	print "<script language = 'javascript'>
	function checkSubmit()
	{
		if (document.form1.name.value == '')
		{
			alert ('Please enter a name');
			return false;
		}
		if (document.form1.email.value == '')
		{
			alert('Please enter an email address');
			return false;
		}
		if (document.form1.phone.value == '')
		{
			alert('Please enter a phone number');
			return false;
		}
		return true;
	}
	</script>";
	background();
	bodyAndLoad();
	$user = param('assigned_to');
	$statement = "select sa_name,sa_login,sa_phone,sa_cell_phone,sa_home_phone,sa_ichat,sa_e_mail,sa_street,sa_city,sa_state,sa_zip, sa_dept, sa_access, sa_permissions from staff where sa_login = '$user'";
	($sa_name,$sa_login,$sa_phone,$sa_cell_phone,$sa_home_phone,$sa_ichat,$sa_e_mail,$sa_street,$sa_city,$sa_state,$sa_zip, $sa_dept, $sa_access, $sa_permissions) = selectValues($statement);
	tableHead('65%');
	print "<form action ='' method = 'post' name='form1' onSubmit= 'return checkSubmit();'>
			<input type='hidden' name='staff' value='updateRes'>
			<input type='hidden' name='original' value='$user'>
			<input type='hidden' name='original_email' value='$sa_e_mail'>
		   <tr><td colspan='2'><center><b>Update profile for $sa_name</b></center></td></tr>
		   <tr><td>Name</td><td><input type='text' name='name' value='$sa_name'></td></tr>
		   <tr><td>Login</td><td><input type='text' name='login' value='$sa_login'></td></tr>
		   <tr><td>Email</td><td><input type='text' name='email' value='$sa_e_mail'></td></tr>
		   <tr><td>iChat</td><td><input type='text' name='ichat' value='$sa_ichat'></td></tr>
		   <tr><td>Office Phone</td><td><input type='text' name='phone' value='$sa_phone'></td></tr>
		   <tr><td>Cell Phone</td><td><input type='text' name='cell_phone' value='$sa_cell_phone'></td></tr>
		   <tr><td>Home Phone</td><td><input type='text' name='home_phone' value='$sa_home_phone'></td></tr>
		   <tr><td>Address</td><td><input type='text' name='address' value='$sa_street'></td></tr>
		   <tr><td>City</td><td><input type='text' name='city' value='$sa_city'></td></tr>
		   <tr><td>State</td><td><input type='text' name='state' value='$sa_state'></td></tr>
		   <tr><td>Zip</td><td><input type='text' name='zip' value='$sa_zip'></td></tr>
		   <tr><td>Access</td><td><select name='sa_access'><option value='Active'>Active</option><option value='Disabled'";
	print "selected" if($sa_access eq "Disabled");
	print ">Disabled</option></select></td></tr>
		   <tr><td>Permissions</td><td><input type='checkbox' name='sa_permissions' ";
	print "checked" if($sa_permissions eq "admin");
	print "> Admin</td></tr>
		   <tr><td>Type</td><td>";
		   dynamicDropDown('staff_type','','staff_type',$sa_dept,'no blank');
		   print "</td></tr>
		   <tr><td colspan = '2'><div align='center'><input type='submit' name='submit' value='Update'></div></td></tr>
		   </table></form>";
	end_html();
}
sub staffCreate()
{
	print $cgi->header();
	headers();
	print "<script language ='javascript'>
	function checkSubmit()
	{
		if (document.form1.name.value == '')
		{
			alert('Please enter a name for this staff member');
			return false;
		}
		if (document.form1.login.value == '')
		{
			alert('Please enter a login name');
			return false;
		}
		if (document.form1.email.value == '')
		{
			alert('Please enter an email address');
			return false;
		}
		if (document.form1.ichat.value == '')
		{
			alert('Please enter an iChat name');
			return false;
		}
		if (document.form1.login.value == '')
		{
			alert('Please enter a login name');
			return false;
		}
	}</script>";
		
	background();
	bodyAndLoad();
	tableHead('65%');
	print "<form action ='' method = 'post' name='form1' onSubmit= 'return checkSubmit();'>
			<input type='hidden' name='staff' value='createRes'>
	<tr><td colspan='2'><center><b>Create new staff member</b></center></td></tr>
		   <tr><td>Name</td><td><input type='text' name='name' value='$sa_name'></td></tr>
		   <tr><td>Login</td><td><input type='text' name='login' value='$sa_login'></td></tr>
		   <tr><td>Email</td><td><input type='text' name='email' value='$sa_e_mail'></td></tr>
		   <tr><td>iChat</td><td><input type='text' name='ichat' value='$sa_ichat'></td></tr>
		   <tr><td>Office Phone</td><td><input type='text' name='phone' value='$sa_phone'></td></tr>
		   <tr><td>Cell Phone</td><td><input type='text' name='cell_phone' value='$sa_cell_phone'></td></tr>
		   <tr><td>Home Phone</td><td><input type='text' name='home_phone' value='$sa_home_phone'></td></tr>
		   <tr><td>Address</td><td><input type='text' name='address' value='$sa_street'></td></tr>
		   <tr><td>City</td><td><input type='text' name='city' value='$sa_city'></td></tr>
		   <tr><td>State</td><td><input type='text' name='state' value='$sa_state'></td></tr>
		   <tr><td>Zip</td><td><input type='text' name='zip' value='$sa_zip'></td></tr>
		   <tr><td colspan = '2'><div align='center'><input type='submit' name='submit' value='Update'></div></td></tr></table></form>";
		   end_html();
}
sub staffCreateRes()
{
	print $cgi->header();
	$id = selectValues("select max(id_num) from staff");
	$id++;
	
	$sa_ichat = param('ichat');
	$sa_email = lc(param('email'));
	$sa_login = param('login');
	$sa_name = param('name');
	$sa_phone = param('phone');
	$sa_cell_phone = param('cell_phone');
	$sa_home_phone = param('home_phone');
	$sa_address = param('address');
	$sa_city = param('city');
	$sa_state = param('state');
	$sa_zip = param('zip');
	$sa_access = param('sa_access');
	$sa_name = quoteValues($sa_name);
	$sa_address = quoteValues($sa_address);
	$statement = "insert into staff (id_num,sa_name,sa_login,sa_e_mail,sa_ichat,sa_phone,sa_cell_phone,sa_home_phone,sa_street,sa_city,sa_state,sa_zip,sa_access) values ($id,$sa_name,'$sa_login','$sa_email','$sa_ichat',
				  '$sa_phone','$sa_cell_phone','$sa_home_phone',$sa_address,'$sa_city','$sa_state','$sa_zip','Active')";
	insert($statement);

	headers();
	background();
	bodyAndLoad();
	ioiFont("The staff member $sa_name has been submitted successfully");
	end_html();
}
		   
sub staffUpdateRes()
{
	print $cgi->header();
	$original_user = param('original');
	$sa_email = lc(param('email'));
	$original_email = param('original_email');
	$sa_login = param('login');
	$statement = "select sa_login from staff where sa_login = '$original_user' and sa_e_mail <> '$original_email'";
	$check_duplicate = selectValues($statement);
	print $cgi->redirect("management.cgi?assigned_to=$original_user&staff=update") if ($check_duplicate ne "");
	$sa_ichat = param('ichat');
	$sa_name = param('name');
	$sa_phone = param('phone');
	$sa_cell_phone = param('cell_phone');
	$sa_home_phone = param('home_phone');
	$sa_address = param('address');
	$sa_city = param('city');
	$sa_state = param('state');
	$sa_zip = param('zip');
	$sa_access = param('sa_access');
	$sa_privelages = param('sa_permissions');
	$sa_privelages = "admin" if ($sa_privelages);
	$sa_privelages = "staff" if (!$sa_privelages);
	$sa_type = param('staff_type');
	$sa_name = quoteValues($sa_name);
	$sa_address = quoteValues($sa_address);
	$statement = "update staff set sa_login = '$sa_login', sa_name = $sa_name, sa_ichat = '$sa_ichat',sa_e_mail = '$sa_email',sa_phone='$sa_phone',sa_cell_phone='$sa_cell_phone',sa_home_phone='$sa_home_phone',
		   sa_street = $sa_address,sa_city='$sa_city',sa_state='$sa_state',sa_zip='$sa_zip',sa_access='$sa_access', sa_permissions='$sa_privelages',sa_dept = '$sa_type' where sa_login='$original_user'";
	#print "$statement";
	insert($statement);
	
	headers();
	background();
	bodyAndLoad();
	ioiFont("'$sa_name' has been updated, click <a href='management.cgi?staff=update&assigned_to=$sa_login'>here</a> to update your recently modified staff member. <p>Click <a href='management.cgi'>here</a> to go back to the management page.");
	end_html();
}
sub emailReaderOptions()
{
	open(OPTIONS,"/Library/WebServer/readerOptions");
	@options = <OPTIONS>;
	foreach $option(@options)
	{
		$db_host = $' if ($option =~ /DB_HOST:/);
		$db_name = $' if ($option =~ /DB_NAME:/);
		$db_user = $' if ($option=~ /DB_USERNAME:/);
		$db_pass = $' if ($option =~ /DB_PASSWORD:/);
		$email_host = $' if ($option =~ /EMAIL_HOST:/);
		$email_user = $' if ($option =~ /EMAIL_USERNAME:/);
		$email_pass = $' if ($option =~ /EMAIL_PASSWORD:/);
		$time_interval = $' if ($option =~ /TIME_INTERVAL:/);
		$ignore_email = $' if ($option =~/IGNORE_MAIL:/);
		$attachments_dir = $' if ($option =~/ATTACHMENTS_DIR:/);
		$error_msg_folder = $' if ($option =~ /ERROR_MSG_FOLDER:/);
		$reminder_interval = $' if ($option =~ /REMINDER_INTERVAL:/);
		$auto_response = $' if ($option =~ /AUTO_RESPONSE:/);
		$supplier_domains = $' if ($option =~ /SUPPLIER_DOMAINS:/);
	}
        chomp($db_host);
        chomp($supplier_domains);
        chomp($db_name);
        chomp($db_user);
        chomp($db_pass);
        chomp($email_host);
        chomp($email_user);
        chomp($email_pass);
        chomp($attachments_dir);
        chomp($time_interval);
        chomp($error_msg_folder);
        chomp($ignore_email);
        chomp($reminder_interval);
        $auto_response =~ s/\[n\]/\n/g;
	

	print $cgi->header();
	headers();
	background();
	bodyAndLoad();
	my $result = `ps -ajwx | grep ioiEmailReader2`;
	ioiFont("DO NOT CHANGE unless you know what you are doing");
	tableHead('65%');
	print "<tr><td colspan ='2'><div align='center'> <font color ='red'>Email Reader is ";
	print "NOT " unless ($result =~ /ioiEmailReader2\.pl/);
	print "Running";
		print"
		<form name='form1' action ='' method ='post' id='form1'>
		<input type = 'hidden' name='manageReader' value='manageRes'>
		  <tr><td>Database Host</td><td><input type='text' name='db_host' value='$db_host'></td></tr>
		  <tr><td>Database Name</td><td><input type='text' name='db_name' value='$db_name'></td></tr>
		  <tr><td>Database User</td><td><input type='text' name='db_user' value='$db_user'></td></tr>
		  <tr><td>Database Password</td><td><input type='password' name='db_pass' value='$db_pass'></td></tr>
		  <tr><td>Email Host</td><td><input type='text' name='email_host' value='$email_host'></td></tr>
		  <tr><td>Email User</td><td><input type='text' name='email_user' value='$email_user'></td></tr>
		  <tr><td>Email Password</td><td><input type='text' name='email_pass' value='$email_pass'></td></tr>
		  <tr><td>Time Interval</td><td><input type='text' name='time_interval' value='$time_interval'></td></tr>
		  <tr><td>Ignored Emails</td><td><input type='text' name='ignore_email' size='40' value='$ignore_email'>(Seperate by commas)</td></tr>
		  <tr><td>Supplier Domains</td><td><input type='text' name='supplier_domains' size='50' value='$supplier_domains'></td></tr>
		  <tr><td>Attachment Directory</td><td><input type='text' size='40' name='attachment_dir' value='$attachments_dir'></td></tr>
		  <tr><td>Error Message Box</td><td><input type='text' name='error_msg_folder' value='$error_msg_folder'></td></tr>
		  <tr><td>Ticket Reminder Interval (minutes)</td><td><input type='text' name='reminder_interval' value='$reminder_interval'>
		  <tr><td colspan = '2'><div align='center'>Auto Response Text</div></td></tr>
		  <tr><td colspan = '2'><div align='center'><textarea rows='10' cols='75' name='auto_response'>$auto_response</textarea></div></td></tr>
		  <tr><td colspan='2'><div align='center'><input type='submit' name='submit' value='Submit'></div></td></tr>
		  </form>
		  </table>";
		  end_HTML();
}
sub manageReaderRes()
{
print $cgi->header();
	headers();
	background();
	$db_host = param('db_host');
	$db_name = param('db_name');
	$db_user = param('db_user');
	$db_pass = param('db_pass');
	$email_host = param('email_host');
	$email_user = param('email_user');
	$email_pass = param('email_pass');
	$time_interval = param('time_interval');
	$ignore_email = param('ignore_email');
	$attachment_dir = param('attachment_dir');
	$error_msg_folder = param('error_msg_folder');
	$reminder_interval = param('reminder_interval');
	$supplier_domains = param('supplier_domains');
	$auto_response = param('auto_response');
	$auto_response =~ s/\n/\[n\]/g;
	
	open(OPTIONS,"/Library/WebServer/readerOptions") or die "could not open options file";
	@options = <OPTIONS>;
	close OPTIONS;
	foreach $option (@options)
	{
		$option = "DB_HOST:" . $db_host if ($option =~ /DB_HOST:/);
		$option = "DB_NAME:" . $db_name if ($option =~ /DB_NAME:/);
		$option = "DB_USERNAME:" . $db_user if ($option=~ /DB_USERNAME:/);
		$option = "DB_PASSWORD:" . $db_pass if ($option =~ /DB_PASSWORD:/);
		$option = "EMAIL_HOST:" . $email_host if ($option =~ /EMAIL_HOST:/);
		$option = "EMAIL_USERNAME:" . $email_user if ($option =~ /EMAIL_USERNAME:/);
		$option = "EMAIL_PASSWORD:" . $email_pass if ($option =~ /EMAIL_PASSWORD:/);
		$option = "TIME_INTERVAL:" . $time_interval if ($option =~ /TIME_INTERVAL:/);
		$option = "IGNORE_MAIL:" .  $ignore_email if ($option =~/IGNORE_MAIL:/);
		$option = "ATTACHMENTS_DIR:" . $attachment_dir if ($option =~/ATTACHMENTS_DIR:/);
		$option = "ERROR_MSG_FOLDER:" . $error_msg_folder if ($option =~ /ERROR_MSG_FOLDER:/);
		$option = "REMINDER_INTERVAL:" . $reminder_interval if ($option =~ /REMINDER_INTERVAL:/);
		$option = "AUTO_RESPONSE:" . $auto_response if ($option =~ /AUTO_RESPONSE:/);
		$option = "SUPPLIER_DOMAINS:" . $supplier_domains if ($option =~ /SUPPLIER_DOMAINS:/);
	}
	open(OPTIONS,">/Library/WebServer/readerOptions") or die "could not open file for writing. Error: $!";
	foreach $option (@options)
	{
		print "$option <p>";
		print OPTIONS $option . "\n";
	}
	close OPTIONS;
	ioiFont("The email reader options have been updated successfully");
}

sub manageUsers($)
{
	my $header = shift;
	print $cgi->header();
	headers();
	background();
	bodyAndLoad();
	ioiFont($header) if ($header);
	tableHead('60%');
	my $statement = "SELECT sub_login, sub_name FROM users";
	my $dbh = getDBConnection();
	my $sth = $dbh->prepare($statement);
	$sth->execute();
	while ( (my $login, my $name ) = $sth->fetchrow_array() ) {
		my $ticketCountStatement = "SELECT count(submitted_by) from problem WHERE submitted_by = '$login'";
		my $ticketCountHandle = $dbh->prepare($ticketCountStatement);
		$ticketCountHandle->execute();
		(my $ticketCount) = $ticketCountHandle->fetchrow_array();
		print "
		<tr><td>$login</td><td>$name</td><td>$ticketCount</td><td><a href='management.cgi?manageUsers=modify&login=$login'>Modify Username</a></td><td><a href='management.cgi?manageUsers=delete&login=$login'>Delete user</a></td></tr>";
	}
	print "</table></body></html>";
}


sub deleteUser()
{
	print $cgi->header();
	headers();
	background();
	bodyAndLoad();
	my $login = param('login');
	my $statement = "SELECT case_num, short_desc, status FROM problem WHERE submitted_by = '$login'";
	my $dbh = getDBConnection();
	my $sth = $dbh->prepare($statement);
	my $count = $sth->execute;
	$count = 0 if ($count eq "0E0");
	print "<div align='center'>The user $login has $count tickets. Are you sure you want to delete.</div><p>";
	if ( $count > 0 ) {
		tableHead('70%');
		print "<tr><td>Ticket #</td><td>Subject</td><td>Status</td></tr>";
		while ( (my $case_num, my $subject, my $status ) = $sth->fetchrow_array() ) {
			print "<tr><td>$case_num</td><td>$subject</td><td>$status</td></tr>";
		}
		print "</table><form name='delete' method='post'>
		<input type='hidden' name='login' value='$login'>
		<input type='hidden' name='manageUsers' value='deleteUserRes'>";
		print "<div align='center'>Reassign tickets to: ";
		customerDropDown($login);
		ioiFont(" Note: This drop down list excludes this user");
		print "<p>Tickets that are not reassigned will marked \"Deleted\" from the database</div><p><div align='center'>
		<input type='submit' name='delete' value='Delete'>
		</form>
		</body></html>";
	} else {
		print "<form name='delete' method='post'>
		<input type='hidden' name='login' value='$login'>
		<input type='hidden' name='manageUsers' value='deleteUserRes'>
		<div align='center'><input type='submit' name='delete' value='Delete'></div>
		</form></body></html>";
	}
}

sub modifyUser($)
{
	print header();
	headers();
	background();
	bodyAndLoad();
	my $message = shift;
	ioiFont($message) if ($message);
	my $login = param('login');
	print "<form name='modify' method='post'>
	<input type='hidden' name='manageUsers' value='modifyUserRes'>
	<input type='hidden' name='login' value='$login'>
	<div align='center'>Change the username $login to <input type='text' name='user_login' value=''></div>
	<p><div align='center'><input type='submit' name='modify' value='Modify'></div>
	</form>
	</body></html>";
}

sub modifyUserRes()
{
	my $old_login = param('login');
	my $new_login = param('user_login');
	my $dbh = getDBConnection();
	my $statement = "SELECT sub_login FROM users WHERE sub_login = '$old_login'";
	my $sth = $dbh->prepare($statement);
	my $count = $sth->execute();
	$count = 0 if ($count eq "0E0");
	print $count;
	if ($count < 1) {
		modifyUser("This user name is already taken, please choose a new username");
	} else {
	insert("UPDATE problem SET submitted_by = '$new_login' WHERE submitted_by = '$old_login'");
	insert("UPDATE users SET sub_login = '$new_login' WHERE sub_login = '$old_login'");
	manageUsers("The login $old_login has been replaced with $new_login");
	}
}

sub deleteUserRes()
{
	my $replacement_user = param('sub_login');
	my $login = param('login');
	if ( $replacement_user ) {
		insert("UPDATE problem SET submitted_by = '$replacement_user' WHERE submitted_by = '$login'");
	} else {
		insert("DELETE FROM problem WHERE submitted_by = '$login'");
	}
	insert("DELETE FROM users WHERE sub_login = '$login'");
	manageUsers("The user $login has been deleted");
}
	
