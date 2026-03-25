tell application "Mail"
    set myMessages to (messages of inbox whose sender contains "openai" and subject contains "data Export is Ready" and date received > ((current date) - 2 * days))
    set output to ""
    repeat with msg in myMessages
        set output to output & "Subject: " & (subject of msg) & linefeed
        set output to output & "Date: " & (date received of msg as string) & linefeed
        set output to output & "Body: " & (content of msg) & linefeed
    end repeat
    return output
end tell
