from django.shortcuts import render
from django.http import JsonResponse
import sys
import json
from io import StringIO



def knzl_view(request):
    if 'runserver' in sys.argv:
        if request.method == 'POST':
            code = request.POST.get('code')  
            captured_output = ""
            output = StringIO()
            error_output = StringIO()
            
            try:
                # Redirect both stdout and stderr
                sys.stdout = output
                sys.stderr = error_output
                exec(code)
            except Exception as e:
                print(f"Error: {e}", file=error_output)
            finally:
                # Always restore stdout and stderr
                sys.stdout = sys.__stdout__
                sys.stderr = sys.__stderr__
            
            # Combine output and errors
            captured_output = output.getvalue()
            error_content = error_output.getvalue()
            
            if error_content:
                captured_output += error_content
            
            captured_output = captured_output.strip()
            
            # Check if this is an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'output': captured_output,
                    'success': True,
                    'has_error': bool(error_content)
                })
            else:
                # Regular form submission (fallback)
                return render(request, 'knzl1.html', {'out': captured_output, 'code':code})
        else:
             return render(request, 'knzl1.html')
    else:
        print("La aplicación está en entorno de producción.")
        return render(request, 'notWorking.html')
    
def knzl_command(request):

    print("Test running !!!")
    return render(request, 'notWorking.html')
