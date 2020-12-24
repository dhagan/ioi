#!/usr/bin/perl

################################################################################
#
#       File Name: FilterTickets.cgi
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

use DBI;
use CGI;

$cgi = new CGI;
$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";
print $cgi->header();
headers();
$user = $ENV{"REMOTE_USER"};
$user =~ s/IOINTEGRATION\\//g;
my $dbh = getDBConnection();
$dbh-> {'LongReadLen'} = 100000000; 
print "<div align='center'><b>Unassigned Tickets:</b></div>";	
print "<style type='text/css'>
		<!--
		body {
			background-color: #C0C0C0;
		}
		
		-->
		</style>";

menu_focus();
bodyAndLoad("menu_focus(document.Form1.assigned_to,\"$user\")");
$skey = $cgi->param('skey');
$ip_remote_user = $cgi->param('ip_remote_user');
print "<script type=text/javascript>
// The time out value is set to be 10,000 milli-seconds (or 10 seconds)
//setTimeout(' document.location=document.location' ,200000);
</script>";

print "<script language='JavaScript'>
function checkUncheckAll() {
var i;
	if(document.Form1.checkall.checked)
	{		
		for (i = 0; i < document.Form1.selrow.length; i++)
		document.Form1.selrow[i].checked = true;
	}
	else
	{
	for (i = 0; i < document.Form1.selrow.length; i++)
		document.Form1.selrow[i].checked = false;
	}
		
}
function deleteButton()
{
	var agree=confirm('Are you sure you want to delete these tickets?');
	if (agree)
	{
		document.Form1.action = 'deleteTickets.cgi';
		document.Form1.submit();
		return true;
	}
	else
	{	
	return false;
	}
}
function assignButton()
{
	var check = document.Form1.assigned_to.value;

	if(check != '')
	{
		document.Form1.action = 'assignTickets.cgi';
		document.Form1.submit();
		return true;
	}
	else
	{
		alert('Please select a IOI tech to assign this ticket to.');
		return false;
	}
}
function changeContactButton()
{
	var j = 0;
	for (var i = 0; i < document.Form1.selrow.length; i++)
	{
		if(document.Form1.selrow[i].checked)
		{
			j++;
			
		}
	}
	if (document.Form1.selrow.length == null)
	{
		if (document.Form1.selrow.checked)
		{
			j=1;
		}
	}		
	if(j == 0)
	{
		alert('Please select the ticket you want to change the contact for');
		return false;
	}
	else if(j > 1)
	{
		alert('Only one contact can be changed at a time');
		return false;
	}
	else
	{
	document.Form1.action = 'changeContact.cgi';
	document.Form1.submit();
	return true;
	}
}
	
function appendButton()
{
	var j = 0;
	for (var i = 0; i < document.Form1.selrow.length; i++)
	{
		if(document.Form1.selrow[i].checked)
		{
			j++;
			
		}
	}
	if (document.Form1.selrow.length == null)
	{
		if (document.Form1.selrow.checked)
		{
			j=1;
		}
	}		
	if(j == 0)
	{
		alert('Please select the ticket you want to append');
		return false;
	}
	else if(j > 1)
	{
		alert('Only one ticket can be appended at a time');
		return false;
	}
	else
	{
	document.Form1.action = 'appendTicket.cgi';
	document.Form1.submit();
	return true;
	}
}
</script>";

print "<center>

<form name='Form1' method= 'get'>
<table width='95%'  border='1' cellpadding='0' cellspacing='0' bordercolor='#C0C0C0' bgcolor='#909090'>
                		<tr bordercolor='#909090'>
                    		<td>
                 				<input type='checkbox' name='checkall' onclick='checkUncheckAll()'>
                    		</td>
                    		<td>
                    			<B>
                    				<font size='2' face='Tahoma, Verdana, Arial, Helvetica'>
                    					Select All
                    				</FONT>
                    			</B>
                    		</td>
                    		<td WIDTH='15'>
                    		</td>
                    		<td>
                    			<B>
                    				<font size='2' face='Tahoma, Verdana, Arial, Helvetica'>
                    					Assign Ticket To:&nbsp;
                    				</FONT>
                    			</B>
                    		</td>
                    		<td>
                				<SELECT NAME='assigned_to' SIZE='1' CLASS='formfield'><option value=''></option>";
                				$sth = $dbh->prepare("select sa_name,sa_login from staff where sa_dept = 'IT' and sa_access <> 'Disabled' order by sa_name");
                				$sth->execute();
                				while(($sa_name,$sa_login) = $sth->fetchrow_array())
                				{
                					print "<option value='$sa_login'>$sa_name</option>";
                				}
               
                		print"
                				
                				</SELECT>
             	   		</td>
             	   		<td>
             	   		<B>
             	   			<input type = 'submit' value = 'Assign' name = 'Assign' onClick='return assignButton();'>
             	   			</td>
             	   		<td>
             	   			<B>
             	   			<input type = 'submit' value = 'Delete' name = 'Delete' onClick='return deleteButton();'>
             	   			</B>
             	   			
             	   			</td>
             	   		<td>
             	   			<B><input type = 'submit' value = 'Append' name = 'Append' onClick='return appendButton();'></B></td>
						<td> <div align='center'><input type='submit' value='Change Contact' name='Change Contact' onclick ='return changeContactButton()'></div></td>
             	   				
                		</tr>

                <td align='center' bgcolor='#909090'valign='middle'>
        	<strong>
	        <font size='2' face='Tahoma, Verdana, Arial, Helvetica' color='#C0C0C0'>
		        Select
	        </font>
      	  </strong>
        </td>
        <td align='center' bgcolor='#909090'valign='middle'>
	        <strong>
      		  	<font size='2' face='Tahoma, Verdana, Arial, Helvetica' color='#C0C0C0'>
			  		Update
		      	</font>
	        </strong>
        </td>
        <td align='center' bgcolor='#909090'valign='middle'>
      	  <strong>
		        <font size='2' face='Tahoma, Verdana, Arial, Helvetica' color='#C0C0C0'>
			        	Ticket Number
			        </a>
		        </font>
	        </strong>
        </td>
        <td align='center' bgcolor='#909090'valign='middle'>
      	  <strong>
		        <font size='2' face='Tahoma, Verdana, Arial, Helvetica' color='#C0C0C0'>
			     
			        	Status
			        
		        </font>
	        </strong>
        </td>
        <td align='center' bgcolor='#909090'nowrap valign='middle'>
      	 	<strong>
		 		<font size='2' face='Tahoma, Verdana, Arial, Helvetica' color='#C0C0C0'>
			   		Date Open
		      	</font>
	      	</strong>
        </td>

        <td align='center' bgcolor='#909090'nowrap valign='middle'>
      	 	<strong>
		 		<font size='2' face='Tahoma, Verdana, Arial, Helvetica' color='#C0C0C0'>
			   		Ticket Submitter
		      	</font>
	      	</strong>
        </td>
        <td align='center' bgcolor='#909090'valign='middle'>
	     	<strong>
		        <font size='2' face='Tahoma, Verdana, Arial, Helvetica' color='#C0C0C0'>
			        Product
		        </font>
	    	</strong>
        </td>
        <td align='center' bgcolor='#909090'valign='middle'>
	     	<strong>
      		  	<font size='2' face='Tahoma, Verdana, Arial, Helvetica' color='#C0C0C0'>
			   
			   			Priority
			   		
		    	</font>
	    	</strong>
        </td>
        <td align='center' bgcolor='#909090'valign='middle'>
      	  	<strong>
		     	<font size='2' face='Tahoma, Verdana, Arial, Helvetica' color='#C0C0C0'>
			   		Short Description
		    	</font>
	       </strong>
        </td>
    </tr>
    ";


$sth = $dbh->prepare("SELECT case_num, submitted_by, date_open, prob_comp_link, short_desc, priority_type, prob_prod_link, status, time_mod FROM problems WHERE assigned_to = 'nobody' and status <> 'Closed'");
$sth->execute();
$userName= $dbh->prepare("SELECT sub_e_mail FROM users WHERE sub_login = ?");
$i = 1;
while(($case_num,$submitted_by, $date_open, $prob_comp_link, $short_desc, $priority, $prob_prod_link, $status,$time_mod) = $sth->fetchrow_array)
{
	$product = $dbh->prepare("SELECT prod_name FROM product WHERE prod_case_num = '$prob_prod_link'");
	$product->execute();
	$prod_name = $product->fetchrow_array();
	$product->finish();
	$date_open =~ s/00:00:00//;
	print "<tr bgcolor='#B0B0B0'><td align='center' valign='middle' nowrap><input TYPE='checkbox' NAME='selrow' VALUE='$case_num'>
	</td>
    	<td align='center' valign='middle' nowrap>
				<strong>
			        	<font size='2' face='Tahoma, Verdana, Arial, Helvetica'>
							<a href= 'respondTicket.cgi?viewTicket=true&case_num=$case_num'>View</a>
						</font>
		        	</strong>
      	</td>
      	<td>
	    	<p align='left'>
      			<font color='#000000'size='2' face='Tahoma, Verdana, Arial, Helvetica'>
			     	$case_num
		      	</font>
	      	</p>
      	</td>
     	<td>
  		 	<font size='2' color='#000000'face='Tahoma, Verdana, Arial, Helvetica'>
			 $status
		   	</font>

	   </td>
      	<td align='center'>
       	<font color='#000000'size='2' face='Tahoma, Verdana, Arial, Helvetica'>
        		$date_open $time_mod
        	</font>
        </td>
      	<td>
       	<font color='#000000'size='2' face='Tahoma, Verdana, Arial, Helvetica'>
        		$submitted_by
        	</font>
        </td>
        <td>
        	<font color='#000000'size='2' face='Tahoma, Verdana, Arial, Helvetica'>
        		$prod_name
        	</font>
        </td>
          <td>
        	<font color='#000000'size='2' face='Tahoma, Verdana, Arial, Helvetica'>
        		$priority
        	</font>
        </td>
        <td>
       	 <font color='#000000'size='2' face='Tahoma, Verdana, Arial, Helvetica'>
			$short_desc
       	 </font>
        </td><tr>";
       }
    print "</table><div align='center'><font color='#808080'><Strong>This page will auto refresh every 2 minutes</strong></font></div>";
  
    $userName->finish();
    $sth->finish();
    
    $dbh->disconnect();
    print $cgi->end_html();