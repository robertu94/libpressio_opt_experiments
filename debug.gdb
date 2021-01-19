set pagination off
start
break exit if status != 0
break pressio_opt.cc:116
commands
print thread_compressor._M_ptr
print thread_compressor._M_ptr.metrics_plugin.plugin._M_ptr
print compressor.plugin._M_ptr
print compressor.plugin._M_ptr.metrics_plugin.plugin._M_ptr
end
continue
