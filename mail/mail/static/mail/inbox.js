document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);


  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#detail-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // call the send mail function to send mail
  send_mail()
}


function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#detail-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // call malbox function
  mail_box(mailbox)
}


// function tosend a mail
function send_mail() {

  document.querySelector('form').onsubmit = function() {
    // get recepient(s)
    let receiver = document.querySelector('#compose-recipients').value;
    let title = document.querySelector('#compose-subject').value;
    let body = document.querySelector('#compose-body').value;    
    
      fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: receiver,
            subject: title,
            body: body
        })
      })
      .then(response => response.json())
      .then(result => {
            // load the sent box
            load_mailbox('sent');       
      });
            return false;
    }  
}


function mail_box(mailbox) {
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

      
      for (let email of emails) {
        const element = document.createElement('div');
        element.innerHTML += 'Sender: ' + email.sender + '<br/>';
        element.innerHTML += 'Subject: ' +  email.subject + '<br/>';
        element.innerHTML += 'Date: ' +  email.timestamp + '<br/>';
        element.innerHTML += '<hr>';
        // change background for read and unread
        if(email.read === true) {
          element.style.backgroundColor = 'gray';
        } else {
          element.style.backgroundColor = 'white';
        }
        // to view the body of the mail run the view_mail function
        element.addEventListener('click', () => view_mail(email));
        element.addEventListener('click', () => arch_unarch(mailbox, email));
        element.addEventListener('click', () => reply_mail(mailbox, email));
        document.querySelector('#emails-view').append(element);
        document.querySelector('#detail-view').innerHTML = '';
        
      }
});
}



function view_mail(email) {
  // Show the detail box and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#detail-view').style.display = 'block';
     
        fetch(`/emails/${email.id}`)
        .then(response => response.json())
        .then(email => {

            const element1 = document.createElement('div');
            element1.innerHTML += 'Sender: ' + email.sender + '<br/>';
            // iterate over list of recepients
            for(let receiver of email.recipients) {
              element1.innerHTML += 'Recipient(s): ' + receiver + '<br/>';
            }
            element1.innerHTML += 'Subject: ' +  email.subject + '<br/>';
            element1.innerHTML += 'Date: ' +  email.timestamp + '<br/>';
            element1.innerHTML += '<hr>';
            element1.innerHTML += 'Body: ' + email.body + '<br/>';
           
            // mark mail as read with an API PUT request
            fetch(`/emails/${email.id}`, {
              method: 'PUT',
              body: JSON.stringify({
                  read: true
              })
            })
            document.querySelector('#detail-view').append(element1); 
           
        });
        
}

// function to archive and unarchive
function arch_unarch(mailbox, email) {
  if (mailbox != 'sent') { 

    const element2 = document.createElement('button');
    element2.setAttribute('class', 'btn btn-sm btn-outline-primary mr-2');
    // check if mailbox is archived unarchived
    if (mailbox == 'inbox') {
      element2.textContent = 'Archive';
    } else if (mailbox == 'archive') {
      element2.textContent = 'Unarchive';
    }

    document.querySelector('#detail-view').append(element2);
    element2.addEventListener('click', () => {
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: !(email.archived)
        })
      }).then(() => load_mailbox('inbox'));
    })
  }
}



// function to reply email
function reply_mail (mailbox, email) {
  if (mailbox == 'inbox') {

    const element3 = document.createElement('button');
    element3.setAttribute('class', 'btn btn-sm btn-outline-primary mr-2');
    element3.textContent = 'Reply';
   
    document.querySelector('#detail-view').append(element3);
    element3.addEventListener('click', () => {
    compose_email()
    // prefill the forms
    document.querySelector('#compose-recipients').value = email.sender;
    if (email.subject.slice(0, 3) == 'Re:') {
      document.querySelector('#compose-subject').value = email.subject;
    } else {
      document.querySelector('#compose-subject').value = 'Re:' + email.subject;
    }
    // "On Jan 1 2020, 12:00 AM foo@example.com wrote:"
    document.querySelector('#compose-body').value = 'On ' + email.timestamp + ' ' + email.sender + ' wrote: '  + email.body;
    });
  }
}