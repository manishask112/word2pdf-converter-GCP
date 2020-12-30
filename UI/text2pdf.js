var src = '';

function generatePDF() {
    var x = document.getElementById("mailID");
    var text_url = document.querySelector('#url').value;
    var textAnalyserURL = "https://us-central1-manisha-suresh.cloudfunctions.net/fetch-text";
    // x.style.display = "none";
    console.log("Tiggering cloud function");
    var xmlHttp = new XMLHttpRequest(); // creates 'ajax' object
        xmlHttp.onreadystatechange = function() //monitors and waits for response from the server
        {
           if(xmlHttp.readyState === 4 && xmlHttp.status === 200) //checks if response was with status -> "OK"
           {
               var re = JSON.parse(xmlHttp.responseText); //gets data and parses it, in this case we know that data type is JSON.

               if(re)
               {
                    console.log("received response!");
                    src = re["textFileName"]
                    console.log("converted to PDF: " + src);
                    var p = document.createElement('p');
                    var text = document.createTextNode("PDF generated as '" + src + "'!\n");
                    p.appendChild(text);
                    x.prepend(p);
                    x.style.display = "block";
               }
               else{
                    console.log("ERROR")
               }
           }
    
        }
        xmlHttp.open("POST", textAnalyserURL); //set method and address
        xmlHttp.send(JSON.stringify({"url":text_url})); //send data    
    }
 
function sendMail() {
    var x = document.getElementById("mailID");
    var mailID = document.querySelector('#email').value;
    var sendMailURL = "https://us-central1-manisha-suresh.cloudfunctions.net/send-mail";
    console.log("Triggering cloud function");
    var xmlHttp = new XMLHttpRequest(); // creates 'ajax' object
    xmlHttp.onreadystatechange = function() //monitors and waits for response from the server
    {
        if(xmlHttp.readyState === 4 && xmlHttp.status === 200) //checks if response was with status -> "OK"
        {
            var re = JSON.parse(xmlHttp.responseText); //gets data and parses it, in this case we know that data type is JSON.

            if(re)
            {
                console.log("email sent!");
                window.alert("Email has been sent!");
                x.firstChild.remove();
                x.style.display = "none";
            }
            else{
                console.log("ERROR")
            }
        }

    }
    xmlHttp.open("POST", sendMailURL); //set method and address
    xmlHttp.send(JSON.stringify({"pdf":src, "mail" : mailID})); //send data    

}