# where is everything?

function readlink() {
	if type -p greadlink > /dev/null; then
		greadlink "$@"
	else
		command readlink "$@"
	fi
}

top=$( readlink -f $( readlink -f $( dirname $( readlink -f $0 ) ) ) )/..  # where am I
lang_data=$top/langs # where are the langs
lang_list="$( cd $lang_data; ls )"

export wd lang_data lang_list
