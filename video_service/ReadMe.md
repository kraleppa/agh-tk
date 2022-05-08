

Build test img:

     docker build -f Dockerfile.test --tag=test . 

Run test:

    docker run --rm -it -v ${pwd}/src:/build/src/ -v ${pwd}/tests:/build/tests/ test 
