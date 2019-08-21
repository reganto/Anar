function passwordMatch()
{
    password = document.getElementById('password').value;
    confirm = document.getElementById('confirm').value;

    if(password != confirm) {
        document.getElementById('msg').innerHTML = 'not matching';
        document.getElementById('msg').style.color = 'red'; 

    } else {
        document.getElementById('msg').innerHTML = 'matching';
        document.getElementById('msg').style.color = 'green';
    }
}

function xmlhttpPost(strURL) 
{
    var xmlHttpReq = false;
    var self = this;

    self.xmlHttpReq = new XMLHttpRequest();
    self.xmlHttpReq.open('POST', strURL, true);
    self.xmlHttpReq.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    self.xmlHttpReq.onreadystatechange = function() {
        if(self.xmlHttpReq.readyState == 4) {
            updatepage(self.xmlHttpReq.responseText);
        }
    }
    self.xmlHttpReq.send(getquesrystring());
}

function getquesrystring()
{
    var form = document.forms['reg'];
    var username = form.username.value;
    qstr = 'username=' + escape(username);
    return qstr;
}

function updatepage(str)
{
    document.getElementById('result').innerHTML = str;
    document.getElementById('result').style.color = 'red';
}