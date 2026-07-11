# Design Specification: Robust Defensive Input Validation

This specification details security, validation, and defensive programming enhancements to prevent the application from encountering unhandled errors (500 Server Errors) or bypassing data format constraints.

---

## 1. Contact Format Constraints (Indian Mobile Numbers)
- **Rule**: All contact numbers must conform to the format `+91XXXXXXXXXX` (where `X` are digits).
- **Backend check**: Enforced via regular expression `r'^\+91\d{10}$'` inside both registration and profile-editing controllers.
- **Frontend check**: Enforced via `<input type="tel" pattern="^\+91\d{10}$">` in forms.

---

## 2. Integer/Float Parse Protection
- **Rule**: Casting form inputs using `int()` or `float()` must be wrapped in `try...except ValueError` blocks.
- **Action**: When parsing fails, the user is flashed a warning message and redirected back to the form interface.
- Affected inputs:
  - Trek duration (Admin creation, Staff proposal)
  - Max capacity slots (Admin creation, Staff proposal)
  - Price in INR (Admin creation, Staff proposal)
  - Available slots edit (Staff details update)

---

## 3. Date Integrity constraints
- **Rule**: Trek start date must not be after end date.
- **Action**: Add validations checking if `start_date <= end_date`. If not, flash a validation warning and redirect back.
