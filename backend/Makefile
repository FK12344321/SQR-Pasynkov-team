run:
	echo Hello

install:
	pip install fastapi[all]
	pip install fastapi-code-generator

generate_api: # !!! Be careful, your previous code will be rewritten !!!
	fastapi-codegen --input ./api/api.swagger.yaml --output ./ -r
