from agent_my.command import Command

c  = Command('ifconfig')
out = c.run()
print(out)