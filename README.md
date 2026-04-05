# Security Code Auditor OpenEnv

## Description
This environment simulates a real-world security code review process. An AI agent acts as a security auditor, scanning code line-by-line to identify vulnerabilities like hardcoded secrets and SQL injection.

## Observation Space
- `code_line`: The specific string of code being reviewed.
- `line_number`: The position in the file.
- `file_name`: The context of the code.

## Action Space
- `SAFE`: No vulnerability detected.
- `VULNERABLE_SECRET`: Detected a hardcoded API key or password.
- `VULNERABLE_SQL_INJECTION`: Detected unsafe string concatenation in a query.

## Tasks
1. **Easy**: Identify basic hardcoded strings.
2. **Medium**: Detect SQL injection patterns.
3. **Hard**: Perform a full audit with high precision and low false positives.