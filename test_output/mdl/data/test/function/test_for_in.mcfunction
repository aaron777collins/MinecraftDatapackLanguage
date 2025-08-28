data modify storage mdl:variables test_list set value []
data modify storage mdl:variables test_list set value []
data modify storage mdl:variables test_list append value "alpha"
data modify storage mdl:variables test_list append value "beta"
data modify storage mdl:variables test_list append value "gamma"
data modify storage mdl:variables test_list append value "delta"
say "Testing for-in loop:"
# For-in loop over test_list
execute store result storage mdl:temp list_length int 1 run data get storage mdl:variables test_list
execute if data storage mdl:variables test_list run function test:for_in_element_test_list
say "For-in loop completed!"
