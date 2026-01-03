import React, { useState, useCallback } from 'react';
import { sanitizeInput, checkRateLimit } from '@utils/security';
import Button from './Button';
export default function SecureForm({ onSubmit, fields, submitLabel = 'Submit', formName, }) {
    const [formData, setFormData] = useState({});
    const [errors, setErrors] = useState({});
    const [isLoading, setIsLoading] = useState(false);
    const handleChange = useCallback((e) => {
        const { name, value } = e.target;
        const sanitized = sanitizeInput(value);
        setFormData((prev) => ({ ...prev, [name]: sanitized }));
        // Clear error on field change
        if (errors[name]) {
            setErrors((prev) => ({ ...prev, [name]: '' }));
        }
    }, [errors]);
    const handleSubmit = useCallback(async (e) => {
        e.preventDefault();
        // Rate limiting check
        if (!checkRateLimit(`form_${formName}`, 5, 60000)) {
            setErrors({ form: 'Too many attempts. Please try again later.' });
            return;
        }
        // Validation
        const newErrors = {};
        fields.forEach((field) => {
            if (field.required && !formData[field.name]) {
                newErrors[field.name] = `${field.label} is required`;
            }
        });
        if (Object.keys(newErrors).length > 0) {
            setErrors(newErrors);
            return;
        }
        setIsLoading(true);
        try {
            await onSubmit(formData);
            setFormData({});
            setErrors({});
        }
        catch (error) {
            setErrors({ form: 'An error occurred. Please try again.' });
        }
        finally {
            setIsLoading(false);
        }
    }, [formData, fields, formName, onSubmit]);
    return (<form onSubmit={handleSubmit} className="space-y-4">
      {errors.form && <div className="p-4 bg-red-100 text-red-700 rounded">{errors.form}</div>}

      {fields.map((field) => (<div key={field.name}>
          <label htmlFor={field.name} className="block text-sm font-medium text-gray-700 mb-1">
            {field.label} {field.required && '*'}
          </label>
          <input id={field.name} name={field.name} type={field.type || 'text'} value={formData[field.name] || ''} onChange={handleChange} className={`w-full px-4 py-2 rounded border ${errors[field.name] ? 'border-red-500' : 'border-gray-300'} focus:outline-none focus:ring-2 focus:ring-blue-500`} disabled={isLoading}/>
          {errors[field.name] && <p className="mt-1 text-sm text-red-600">{errors[field.name]}</p>}
        </div>))}

      <Button type="submit" variant="primary" fullWidth isLoading={isLoading}>
        {submitLabel}
      </Button>
    </form>);
}
