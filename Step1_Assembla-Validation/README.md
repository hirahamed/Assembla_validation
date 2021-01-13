# First step is to run the assembla_validation.py

It includes the validation for the inputs in assembla.

Below is the list of validations it entertains:


* Attachments names against each activity.

* Http version field.

* Personal vs Corporate.

* Http host (pattern matching).

* Http uri path (pattern matching).

* Login-LoginFail depth verification.

* Response field only be filled for login and login-fail.

* Response should not be filled for another activity.

* Multiple Request methods, then all fields will be of same size.

* Request method should not be empty.

* If request method is NA or REMAINING then all fields should be empty.

* If request method is filled then atleast host should be filled.

* Attachments counts should be same as the activities performed.




