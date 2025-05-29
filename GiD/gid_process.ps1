proc handle_request {channel client_addr client_port} {
    gets $channel request
    set request_parts [split $request " "]
    
    if {[llength $request_parts] < 2} {
        respond $channel 400 "Invalid request"
        return
    }
    
    set path [lindex $request_parts 1]
    
    # Solo conservamos el endpoint gid_process
    if {[string match "/gid_process/*" $path]} {
        # CORRECCIÓN: Usar $path en lugar de $params
        set gid_command [string range $path [string length "/gid_process/"] end]
        set gid_command [string map {"%20" " "} $gid_command]
        
        puts "== Comando GiD: '$gid_command' =="
        
        if {[catch {GiD_Process {*}$gid_command} error_msg]} {
            respond $channel 500 $error_msg
            puts "== Error: $error_msg =="
        } else {
            respond $channel 200 "Comando ejecutado: $gid_command"
        }
    } else {
        respond $channel 404 "Endpoint no válido"
    }
    
    close $channel
}

# Helper para respuestas HTTP
proc respond {channel status message} {
    set status_map {
        200 "OK"
        400 "Bad Request"
        404 "Not Found"
        500 "Internal Server Error"
    }
    puts $channel "HTTP/1.1 $status [dict get $status_map $status]\nContent-Type: text/plain\n\n$message"
}

# Iniciar servidor
catch {close $server}
set server [socket -server handle_request 8888]
puts "✅ Servidor listo en http://localhost:8888"