function passwordMatch()
{
    password = document.getElementById('password').value;
    confirm = document.getElementById('confirm').value;

    if(password != confirm) {
        document.getElementById('msg').innerHTML = 'Not matching';
        document.getElementById('msg').style.color = 'red'; 

    } else {
        document.getElementById('msg').innerHTML = '';
        // document.getElementById('msg').style.color = 'green';
    }
}



function xmlhttpPost(strURL) 
{
    var xmlHttpReq = false;
    var self = this;

    self.xmlHttpReq = new XMLHttpRequest();
    self.xmlHttpReq.open('POST', strURL, true);
    self.xmlHttpReq.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    csrf_token_input = document.getElementById('csrf').firstChild;
    csrf_token = csrf_token_input.getAttribute('value');
    self.xmlHttpReq.setRequestHeader('X-CSRFTOKEN', csrf_token);
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



function sendRequest(data)
{
    var xHRObject = false;
    var self = this;

    self.xHRObject = new XMLHttpRequest();
    self.xHRObject.open('GET', '/usrexist?username=' + data, true);
    self.xHRObject.onreadystatechange = function()
    {
        if(self.xHRObject.readyState == 4 && self.xHRObject.status == 200)
        {
            ninimini(self.xHRObject.responseText)
        }
    }
    self.xHRObject.send(null);
}

function ninimini(response)
{
    document.getElementById('result').innerHTML = response;
    document.getElementById('result').style.color = 'red';
    if(response == 'Username does not exist')
    {
        document.getElementById('loginbtn').setAttribute('disabled', 'disabled');                
    } else {
        document.getElementById('loginbtn').removeAttribute('disabled');                
    }
}
