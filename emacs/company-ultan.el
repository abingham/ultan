;;; company-ultan.el --- company integration for the ultan identifier server. -*- lexical-binding: t -*-
;;
;; Copyright (c) 2017 Austin Bingham
;;
;; Author: Austin Bingham <austin.bingham@gmail.com>
;; Version: 0.0.1
;; URL: https://github.com/abingham/emacs-ultan
;; Package-Requires: ((ultan "20171221"))
;;
;; This file is not part of GNU Emacs.
;;
;;; Commentary:
;;
;; Description:
;;
;; ultan is an identifier server for Python.
;;
;; For more details, see the project page at
;; https://github.com/abingham/ultan.
;;
;;; License:
;;
;; Permission is hereby granted, free of charge, to any person
;; obtaining a copy of this software and associated documentation
;; files (the "Software"), to deal in the Software without
;; restriction, including without limitation the rights to use, copy,
;; modify, merge, publish, distribute, sublicense, and/or sell copies
;; of the Software, and to permit persons to whom the Software is
;; furnished to do so, subject to the following conditions:
;;
;; The above copyright notice and this permission notice shall be
;; included in all copies or substantial portions of the Software.
;;
;; THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
;; EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
;; MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
;; NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
;; BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
;; ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
;; CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
;; SOFTWARE.

;;; Code:

(require 'dash)
(require 's)
(require 'ultan)

(defun company-ultan--prefix ()
  "Find prefix for completion."
  (and
   (not (company-in-string-or-comment))

   ;; TODO: This is wrong. We probably just want to look back to the last
   ;; whitespace or something.
   (or (company-grab-symbol-cons "\\.\\|->\\|::\\|/" 2)
       'stop)))

(defun company-ultan--candidates (prefix)
  "Find ultan candidates that start with `prefix'."
  (cons :async
        (lambda (cb)
          (deferred:$
            (ultan-get-names prefix)
            (deferred:nextc it
              (lambda (rsp)
                (let* ((candidate-vec (request-response-data rsp))
                       (prefixed (seq-filter (-partial 's-starts-with? prefix )
                                             candidate-vec))
                       (candidate-list (append prefixed nil)))
                  (funcall cb candidate-list))))))))

(defun company-ultan (command &optional arg &rest ignored)
  "The company-backend command handler for ultan."
  (interactive (list 'interactive))
  (cl-case command
    (interactive     (company-begin-backend 'company-ultan))
    (prefix          (company-ultan--prefix))
    (candidates      (company-ultan--candidates arg))))

;;;###autoload
(defun company-ultan-setup ()
  "Add company-ultan to the front of company-backends."
  (interactive)
  (add-to-list 'company-backends 'company-ultan))

(provide 'company-ultan)
