export THEANO_FLAGS="floatX=float32,cuda.root=/usr/local/cuda-7.0/,device=gpu,assert_no_cpu_op='raise'"
python use_gpu.py
python train_model.py 'gru'
