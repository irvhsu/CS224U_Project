export THEANO_FLAGS="floatX=float32,device=gpu,assert_no_cpu_op='raise'"

python train_model.py 'lstm'