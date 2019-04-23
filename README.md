# bday-wisher
Birthday Wisher

# config.yaml
Configure email address, username, password and receiptent addresses [can specify multiple address]
e.g:
```yaml
birthday:
    csv: bday.csv
    email:
        subject: "Birthday Wishes to {name}"
        sender:
            userid: "sender@mail.net"
            passwd: "send_password"
        receivers:
            - "recv@mail.net"
        body: "
            Dear %s,
            On Behalf of the our Company Family
            We Wish You A Very Happy Birthday
            
            Cheers,
            From Company Family 
            "
```

# bday.csv
format:
```csv
<name>|<date>|<month>
```
  
Run  _send_bday_wish.py_ using cron every day to send email
