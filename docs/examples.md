# `Monolg` Examples

If you'd like to see more realisic examples monolg, you can find
them in the following repository, which is meant for a more in-depth look into the library and its different use cases

[monolg-examples :fontawesome-brands-github:](https://github.com/Mukhopadhyay/monolg-examples){ .md-button }

## A very impractical code block

```python
import monolg

mlg = Monolg(verbose=True)

mlg.clear_logs()
mlg.clear_sys_logs()

mlg.connect()

mlg.log('This is a log log')
mlg.info('This is a info log')
mlg.warning('This is a warning log')
mlg.error('This is a error log')
mlg.critical('This is a critical log')

mlg.close()
```