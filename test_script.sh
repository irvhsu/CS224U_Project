export THEANO_FLAGS="floatX=float32,cuda.root=/usr/local/cuda-7.0/,device=gpu,assert_no_cpu_op='raise'"

python test_model.py gru.12.3000 snli_1.0/snli_1.0_test_data.pickle test_results.txt
python test_model.py gru.12.3000 snli_1.0/snli_1.0_dev_data.pickle dev_results.txt
python test_model.py gru.12.3000 snli_1.0/snli_1.0_train_data.pickle train_results.txt
