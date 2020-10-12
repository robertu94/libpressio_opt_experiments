set pagination off
start
break exit if status != 0
break dist_grid.cc:57
commands
print lower_bound
print upper_bound
print grid_lower
print grid_upper
end
continue
