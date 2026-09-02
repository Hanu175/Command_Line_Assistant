import subprocess

def get_command_help(command, timeout=5):
    """
    Attempt to retrieve help output from a command.
    
    The function tries common help mechanisms and 
    returns the successful output.
    """
    help_variant = [
        [command, "--help"],
        [command, "-h"],
        [command, "help"],
    ]
    
    for args in help_variant:
        try:
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            
            output  = result.stdout or result.stderr
            
            if output and output.strip():
                return output.strip()
        
        except(
            FileNotFoundError,
            subprocess.TimeoutExpired,
            OSError
        ):
            continue
    return None