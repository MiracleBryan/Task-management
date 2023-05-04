// Utility to return all the local storage attribute keys.

// Access Token
function get_access_token_attr_key() {
    return "access_token"
}

// Dark Mode
function get_dark_mode_attr_key() {
    return "is_dark"
}

// Is Authenticated
function is_authenticated() {
    return localStorage.getItem(get_access_token_attr_key())
}

export { get_access_token_attr_key, get_dark_mode_attr_key, is_authenticated }