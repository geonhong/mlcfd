#!/bin/bash

function check_file_exists()
{
	mid_names=("endPoint" "upper" "front" "lower" "midPoint")

	for mid_name in $mid_names
	do
		targetFile="airfoil.$mid_name"

		if [[ -f ${targetFile}.z0 ]] || [[ -f ${targetFile}.z1 ]]
		then
			true
		fi
	done

	false
}

# Input file
_file='constant/airfoilData/airfoil.dat'

if [ ! -z $1 ]
then
	_file=$1
fi

region_name=("upper" "front" "lower")
rind=0
is_endpt=true

if [ check_file_exists ]
then
	echo "Removing previously generated airfoil data file"
	rm airfoil.*.z?
fi

nlines=$(cat $_file | wc -l)

count=0

if [[ -f "$_file" ]]
then
	while read -r line
	do
		data=$(echo $line | tr "b" " ")
		endchar=${line: -1}

		# Check if the given data is the end point
		count=$(( count + 1 ))
		if [ $count == $nlines ]
		then
			is_endpt=true
		fi

		if $is_endpt				# Write end points
		then
			targetFileName="airfoil.endPoint"
			is_endpt=false
		elif [ "$endchar" == 'b' ] 	# Write mid points
		then
			targetFileName="airfoil.midPoint"
			rind=$(( rind + 1 ))
		else
			targetFileName="airfoil.${region_name[$rind]}"
			dataf=$data
		fi

		# Writing data to corresponding file
		echo "( $data 0 )" >> ${targetFileName}.z0
		echo "( $data 0.1 )" >> ${targetFileName}.z1
	done < "$_file"
fi

if [ check_file_exists ]
then
	echo "Moving manipulated data to 'constant/airfoilData'"
	mv airfoil.*.z? constant/airfoilData
fi

echo
echo "done"
echo
