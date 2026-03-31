#!/bin/bash
echo "ASKPASS: '$*'" >> /tmp/askpass.log
if echo "$*" | grep -q "Username"; then
  echo "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"
else
  echo ""
fi
